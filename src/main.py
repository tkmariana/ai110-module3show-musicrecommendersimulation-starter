"""
Command line runner for the Music Recommender Simulation.

Examples (run from the project root):
    python src/main.py                         # balanced mode, detailed layout
    python src/main.py --mode mood_first       # pick a scoring mode
    python src/main.py --mode all              # run every mode
    python src/main.py --diversity --table     # diversity penalty + summary table
"""

import argparse
import textwrap

from recommender import SCORING_MODES, DEFAULT_MODE, load_songs, recommend_songs

# Normal profiles: clear, consistent tastes
NORMAL_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.90, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.40, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
}

# Adversarial profiles: built to see if the scoring can be tricked
ADVERSARIAL_PROFILES = {
    "Conflicted (sad but wants high energy)": {
        "genre": "classical", "mood": "melancholy", "energy": 0.90, "likes_acoustic": False,
    },
    "Unknown labels (genre/mood not in catalog)": {
        "genre": "k-pop", "mood": "euphoric", "energy": 0.70, "likes_acoustic": False,
    },
    "Acoustic metal (acoustic taste vs. loud genre)": {
        "genre": "metal", "mood": "angry", "energy": 0.97, "likes_acoustic": True,
    },
}

# Uses the advanced song features: mood tags, release decade, popularity, instrumentalness
ADVANCED_PROFILES = {
    "Nostalgic 90s Acoustic": {
        "genre": "country", "mood": "nostalgic", "energy": 0.45, "likes_acoustic": True,
        "mood_tags": ["nostalgic", "warm"], "decade": 1990, "popularity": 50,
        "likes_instrumental": False,
    },
}

BASE_KEYS = ("genre", "mood", "energy", "likes_acoustic")


def show_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5,
                         mode: str = DEFAULT_MODE, diversity: bool = False,
                         table: bool = False) -> None:
    """Print the top k recommendations for one profile in a readable layout."""
    recommendations = recommend_songs(user_prefs, songs, k=k, mode=mode, diversity=diversity)

    line = "=" * 60
    print(f"\n{line}")
    print(f"  PROFILE: {name}")
    print(
        f"  {user_prefs['genre']} / {user_prefs['mood']} / "
        f"energy {user_prefs['energy']} / likes acoustic: {user_prefs['likes_acoustic']}"
    )
    extras = {key: value for key, value in user_prefs.items() if key not in BASE_KEYS}
    if extras:
        print("  extra prefs: " + ", ".join(f"{key}={value}" for key, value in extras.items()))
    print(f"  mode: {mode}  |  diversity penalty: {'on' if diversity else 'off'}")
    print(line)

    if table:
        print(format_table(recommendations))
    else:
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{rank}  {song['title']} by {song['artist']}")
            print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
            print(f"    Score: {score:.2f}")
            print("    Why:")
            for reason in explanation.split("; "):
                print(f"      - {reason}")

    print(f"\n{line}")


def format_table(recommendations: list, reason_width: int = 64) -> str:
    """Return an ASCII table with rank, title, artist, score and the reasons for each song."""
    headers = ["#", "Title", "Artist", "Score", "Reasons"]
    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        reasons = [line for reason in explanation.split("; ")
                   for line in textwrap.wrap(f"- {reason}", reason_width, subsequent_indent="  ")]
        rows.append([str(rank), song["title"], song["artist"], f"{score:.2f}", reasons])

    widths = [
        max(len(headers[i]), *(len(row[i]) for row in rows)) if rows else len(headers[i])
        for i in range(4)
    ] + [reason_width]
    rule = "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def fmt(cells):
        return "| " + " | ".join(cell.ljust(w) for cell, w in zip(cells, widths)) + " |"

    out = [rule, fmt(headers), rule]
    for rank, title, artist, score, reasons in rows:
        out.append(fmt([rank, title, artist, score, reasons[0]]))
        for extra in reasons[1:]:
            out.append(fmt(["", "", "", "", extra]))
        out.append(rule)
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument("--mode", default=DEFAULT_MODE, choices=[*SCORING_MODES, "all"],
                        help="scoring mode (default: balanced)")
    parser.add_argument("--diversity", action="store_true",
                        help="penalize repeated artists and genres in the top results")
    parser.add_argument("--table", action="store_true",
                        help="show results as a summary table")
    args = parser.parse_args()

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    modes = list(SCORING_MODES) if args.mode == "all" else [args.mode]
    profiles = {**NORMAL_PROFILES, **ADVERSARIAL_PROFILES, **ADVANCED_PROFILES}
    for mode in modes:
        for name, prefs in profiles.items():
            show_recommendations(name, prefs, songs, mode=mode,
                                 diversity=args.diversity, table=args.table)


if __name__ == "__main__":
    main()
