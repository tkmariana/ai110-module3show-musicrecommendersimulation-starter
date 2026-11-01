import csv
from typing import List, Dict, Tuple, Optional, Union
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"


@dataclass(frozen=True)
class ScoringMode:
    """One ranking strategy: how many points each rule is worth."""
    name: str
    mood: float
    genre: float
    energy: float
    acoustic: float
    tags: float
    popularity: float
    decade: float
    instrumental: float
    speechiness: float


# Strategy pattern: score_song() stays the same, only the weights it is handed change.
SCORING_MODES: Dict[str, ScoringMode] = {
    "balanced": ScoringMode("balanced", mood=2.0, genre=1.0, energy=2.0, acoustic=1.0,
                            tags=1.5, popularity=0.5, decade=0.5, instrumental=0.5, speechiness=0.5),
    "genre_first": ScoringMode("genre_first", mood=1.0, genre=3.0, energy=1.5, acoustic=1.0,
                               tags=1.0, popularity=0.5, decade=0.5, instrumental=0.5, speechiness=0.5),
    "mood_first": ScoringMode("mood_first", mood=3.0, genre=0.5, energy=1.5, acoustic=1.0,
                              tags=2.0, popularity=0.5, decade=0.5, instrumental=0.5, speechiness=0.5),
    "energy_focused": ScoringMode("energy_focused", mood=1.0, genre=0.5, energy=4.0, acoustic=1.0,
                                  tags=1.0, popularity=0.5, decade=0.5, instrumental=0.5, speechiness=0.5),
}
DEFAULT_MODE = "balanced"


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting numeric columns to int/float and mood_tags to a list."""
    int_fields = ("id", "tempo_bpm", "popularity", "release_decade")
    float_fields = ("energy", "valence", "danceability", "acousticness", "instrumentalness", "speechiness")

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                if field in row:
                    row[field] = int(row[field])
            for field in float_fields:
                if field in row:
                    row[field] = float(row[field])
            if "mood_tags" in row:
                row["mood_tags"] = row["mood_tags"].split("|")
            songs.append(row)
    return songs

def _resolve_mode(mode: Union[str, ScoringMode]) -> ScoringMode:
    """Accept a mode name or a ScoringMode and return the ScoringMode."""
    if isinstance(mode, ScoringMode):
        return mode
    if mode not in SCORING_MODES:
        raise ValueError(f"Unknown mode '{mode}'. Choose from: {', '.join(SCORING_MODES)}")
    return SCORING_MODES[mode]

def score_song(user_prefs: Dict, song: Dict, mode: Union[str, ScoringMode] = DEFAULT_MODE) -> Tuple[float, List[str]]:
    """Score one song against the user's prefs using a scoring mode; return (score, list of reasons)."""
    w = _resolve_mode(mode)
    score = 0.0
    reasons = []

    if song["mood"] == user_prefs.get("mood"):
        score += w.mood
        reasons.append(f"mood match (+{w.mood:.1f})")

    if song["genre"] == user_prefs.get("genre"):
        score += w.genre
        reasons.append(f"genre match (+{w.genre:.1f})")

    if "energy" in user_prefs:
        gap = abs(song["energy"] - user_prefs["energy"])
        points = w.energy * (1 - gap)
        score += points
        reasons.append(f"energy {song['energy']:.2f} is {gap:.2f} from target (+{points:.2f})")

    if "likes_acoustic" in user_prefs:
        target = 0.8 if user_prefs["likes_acoustic"] else 0.2
        gap = abs(song["acousticness"] - target)
        points = w.acoustic * (1 - gap)
        score += points
        reasons.append(f"acousticness {song['acousticness']:.2f} is {gap:.2f} from target (+{points:.2f})")

    # Advanced features: only scored when the user profile asks for them.
    if user_prefs.get("mood_tags"):
        wanted = user_prefs["mood_tags"]
        shared = [t for t in song.get("mood_tags", []) if t in wanted]
        if shared:
            points = w.tags * len(shared) / len(wanted)
            score += points
            reasons.append(f"tags {'+'.join(shared)} match (+{points:.2f})")

    if "popularity" in user_prefs and "popularity" in song:
        gap = abs(song["popularity"] - user_prefs["popularity"])
        points = w.popularity * (1 - gap / 100)
        score += points
        reasons.append(f"popularity {song['popularity']} is {gap} from target (+{points:.2f})")

    if "decade" in user_prefs and "release_decade" in song:
        years = abs(song["release_decade"] - user_prefs["decade"])
        points = w.decade * (1 - min(years / 50, 1.0))
        score += points
        reasons.append(f"decade {song['release_decade']}s is {years} years from {user_prefs['decade']}s (+{points:.2f})")

    if "likes_instrumental" in user_prefs and "instrumentalness" in song:
        target = 0.9 if user_prefs["likes_instrumental"] else 0.1
        gap = abs(song["instrumentalness"] - target)
        points = w.instrumental * (1 - gap)
        score += points
        reasons.append(f"instrumentalness {song['instrumentalness']:.2f} is {gap:.2f} from target (+{points:.2f})")

    if "target_speechiness" in user_prefs and "speechiness" in song:
        gap = abs(song["speechiness"] - user_prefs["target_speechiness"])
        points = w.speechiness * (1 - gap)
        score += points
        reasons.append(f"speechiness {song['speechiness']:.2f} is {gap:.2f} from target (+{points:.2f})")

    return score, reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: Union[str, ScoringMode] = DEFAULT_MODE,
    diversity: bool = False,
    artist_penalty: float = 1.0,
    genre_penalty: float = 0.5,
) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), best first.

    With diversity=True, a song loses points for each already-picked song by the
    same artist (artist_penalty) or in the same genre (genre_penalty).
    """
    scored = [(song, *score_song(user_prefs, song, mode)) for song in songs]

    target_energy = user_prefs.get("energy", 0.0)
    energy_gap = lambda song: abs(song["energy"] - target_energy)

    if not diversity:
        ranked = sorted(scored, key=lambda item: (-item[1], energy_gap(item[0])))[:k]
        return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked]

    picked: List[Tuple[Dict, float, List[str]]] = []
    pool = list(scored)
    while pool and len(picked) < k:
        best = None
        for index, (song, score, reasons) in enumerate(pool):
            same_artist = sum(p[0]["artist"] == song["artist"] for p in picked)
            same_genre = sum(p[0]["genre"] == song["genre"] for p in picked)
            adjusted = score
            notes = []
            if same_artist:
                cut = artist_penalty * same_artist
                adjusted -= cut
                notes.append(f"diversity penalty: artist already listed (-{cut:.1f})")
            if same_genre:
                cut = genre_penalty * same_genre
                adjusted -= cut
                notes.append(f"diversity penalty: genre already listed (-{cut:.1f})")
            key = (-adjusted, energy_gap(song))
            if best is None or key < best[0]:
                best = (key, index, song, adjusted, reasons + notes)
        _, index, song, adjusted, reasons = best
        picked.append((song, adjusted, reasons))
        pool.pop(index)

    return [(song, score, "; ".join(reasons)) for song, score, reasons in picked]
