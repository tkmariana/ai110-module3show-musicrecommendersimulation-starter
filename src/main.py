"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

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


def show_recommendations(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print the top k recommendations for one profile in a readable layout."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    line = "=" * 60
    print(f"\n{line}")
    print(f"  PROFILE: {name}")
    print(
        f"  {user_prefs['genre']} / {user_prefs['mood']} / "
        f"energy {user_prefs['energy']} / likes acoustic: {user_prefs['likes_acoustic']}"
    )
    print(line)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}")
        print(f"    Score: {score:.2f}")
        print("    Why:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")

    print(f"\n{line}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, prefs in {**NORMAL_PROFILES, **ADVERSARIAL_PROFILES}.items():
        show_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
