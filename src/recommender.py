import csv
from typing import List, Dict, Tuple, Optional
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

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting numeric columns to int/float."""
    int_fields = ("id", "tempo_bpm")
    float_fields = ("energy", "valence", "danceability", "acousticness")

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's prefs and return (score, list of reasons)."""
    score = 0.0
    reasons = []

    if song["mood"] == user_prefs.get("mood"):
        score += 2.0
        reasons.append("mood match (+2.0)")

    if song["genre"] == user_prefs.get("genre"):
        score += 1.0
        reasons.append("genre match (+1.0)")

    if "energy" in user_prefs:
        gap = abs(song["energy"] - user_prefs["energy"])
        points = 2.0 * (1 - gap)
        score += points
        reasons.append(f"energy {song['energy']:.2f} is {gap:.2f} from target (+{points:.2f})")

    if "likes_acoustic" in user_prefs:
        target = 0.8 if user_prefs["likes_acoustic"] else 0.2
        gap = abs(song["acousticness"] - target)
        points = 1.0 - gap
        score += points
        reasons.append(f"acousticness {song['acousticness']:.2f} is {gap:.2f} from target (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), best first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    target_energy = user_prefs.get("energy", 0.0)
    ranked = sorted(
        scored,
        key=lambda item: (-item[1], abs(item[0]["energy"] - target_energy)),
    )
    return ranked[:k]
