# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

From what I understand, apps like Spotify keep track of what you listen to, skip, and like, and then recommend songs that are similar to those or that people like you listen to. Mine is a lot simpler. It just checks how close each song is to what the user says they like. I care most about mood and energy, and I want the closest match, not just the highest energy.

**Song features:** genre, mood, energy, valence, acousticness (I'm not using tempo or danceability because they're pretty much the same as energy)

**UserProfile features:** favorite genre, favorite mood, target energy, likes acoustic (yes or no)

**My algorithm recipe:** each song in the CSV gets up to 6 points:

- +2 if the mood matches
- +1 if the genre matches
- up to +2 for energy, using `2 * (1 - |song energy - target energy|)`, so the closer the better
- up to +1 for acousticness, using `1 - |song acousticness - target|` (target is 0.8 if they like acoustic, 0.2 if not)

After that I sort the songs from highest to lowest score (if there's a tie, the one with closer energy wins) and show the top 5 with why they got that score.

**Biases I think it might have:**

- Mood is worth the most, so a song with the right genre and energy but a mood like "relaxed" instead of "chill" could get ranked too low.
- Genre and mood are all or nothing, so close ones get no credit.
- Genre barely matters since most genres only show up once in my small list of songs.
- I'm not scoring valence, so a happy song and an angry song with the same energy can look the same.
- The labels can beat the numbers. Someone who likes classical and melancholy but wants high energy would still get a quiet classical song first.

**Extra features I added later:**

- **5 new song columns:** popularity, release decade, mood tags, instrumentalness, and speechiness. They only count when a user profile asks for them.
- **Scoring modes:** `balanced` (the one above), `genre_first`, `mood_first`, and `energy_focused`. Switch with `python src/main.py --mode mood_first` or use `--mode all`.
- **Diversity penalty:** `--diversity` takes points off a song if its artist or genre is already in the top results.
- **Summary table:** `--table` shows the results in a table with the reasons for each score.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

This is what I get when I run `python src/main.py` with a pop, happy, energy 0.8 profile. It shows the top 5 songs, their scores, and why each one got that score.

```
Loaded songs: 18

============================================================
  TOP 5 RECOMMENDATIONS
  Profile: pop / happy / energy 0.8
============================================================

#1  Sunrise City by Neon Echo
    Genre: pop  |  Mood: happy
    Score: 4.96
    Why:
      - mood match (+2.0)
      - genre match (+1.0)
      - energy 0.82 is 0.02 from target (+1.96)

#2  Rooftop Lights by Indigo Parade
    Genre: indie pop  |  Mood: happy
    Score: 3.92
    Why:
      - mood match (+2.0)
      - energy 0.76 is 0.04 from target (+1.92)

#3  Gym Hero by Max Pulse
    Genre: pop  |  Mood: intense
    Score: 2.74
    Why:
      - genre match (+1.0)
      - energy 0.93 is 0.13 from target (+1.74)

#4  Concrete Jungle by Kid Cipher
    Genre: hip hop  |  Mood: confident
    Score: 1.96
    Why:
      - energy 0.78 is 0.02 from target (+1.96)

#5  Night Drive Loop by Neon Echo
    Genre: synthwave  |  Mood: moody
    Score: 1.90
    Why:
      - energy 0.75 is 0.05 from target (+1.90)

============================================================
```

Sunrise City is first because it matches everything. Rooftop Lights is second because the mood matches even though the genre is indie pop. Gym Hero shows up third just because it's pop, even though it's an intense song and not a happy one. That's the genre bias I was worried about.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Profile Evaluation Output

I tried 3 normal profiles and 3 tricky ones to see if I could trick it. This is the top 5 for each.

### High-Energy Pop (Normal)

```
============================================================
  PROFILE: High-Energy Pop
  pop / happy / energy 0.9 / likes acoustic: False
============================================================

#1  Sunrise City by Neon Echo
    Genre: pop  |  Mood: happy
    Score: 5.82
    Why:
      - mood match (+2.0)
      - genre match (+1.0)
      - energy 0.82 is 0.08 from target (+1.84)
      - acousticness 0.18 is 0.02 from target (+0.98)

#2  Rooftop Lights by Indigo Parade
    Genre: indie pop  |  Mood: happy
    Score: 4.57
    Why:
      - mood match (+2.0)
      - energy 0.76 is 0.14 from target (+1.72)
      - acousticness 0.35 is 0.15 from target (+0.85)

#3  Gym Hero by Max Pulse
    Genre: pop  |  Mood: intense
    Score: 3.79
    Why:
      - genre match (+1.0)
      - energy 0.93 is 0.03 from target (+1.94)
      - acousticness 0.05 is 0.15 from target (+0.85)

#4  Storm Runner by Voltline
    Genre: rock  |  Mood: intense
    Score: 2.88
    Why:
      - energy 0.91 is 0.01 from target (+1.98)
      - acousticness 0.10 is 0.10 from target (+0.90)

#5  Neon Pulse by Circuit Haze
    Genre: edm  |  Mood: energetic
    Score: 2.73
    Why:
      - energy 0.95 is 0.05 from target (+1.90)
      - acousticness 0.03 is 0.17 from target (+0.83)

============================================================
```

What I expected. Gym Hero and Storm Runner show up just because the energy is close.

### Chill Lofi (Normal)

```
============================================================
  PROFILE: Chill Lofi
  lofi / chill / energy 0.4 / likes acoustic: True
============================================================

#1  Midnight Coding by LoRoom
    Genre: lofi  |  Mood: chill
    Score: 5.87
    Why:
      - mood match (+2.0)
      - genre match (+1.0)
      - energy 0.42 is 0.02 from target (+1.96)
      - acousticness 0.71 is 0.09 from target (+0.91)

#2  Library Rain by Paper Lanterns
    Genre: lofi  |  Mood: chill
    Score: 5.84
    Why:
      - mood match (+2.0)
      - genre match (+1.0)
      - energy 0.35 is 0.05 from target (+1.90)
      - acousticness 0.86 is 0.06 from target (+0.94)

#3  Spacewalk Thoughts by Orbit Bloom
    Genre: ambient  |  Mood: chill
    Score: 4.64
    Why:
      - mood match (+2.0)
      - energy 0.28 is 0.12 from target (+1.76)
      - acousticness 0.92 is 0.12 from target (+0.88)

#4  Focus Flow by LoRoom
    Genre: lofi  |  Mood: focused
    Score: 3.98
    Why:
      - genre match (+1.0)
      - energy 0.40 is 0.00 from target (+2.00)
      - acousticness 0.78 is 0.02 from target (+0.98)

#5  Coffee Shop Stories by Slow Stereo
    Genre: jazz  |  Mood: relaxed
    Score: 2.85
    Why:
      - energy 0.37 is 0.03 from target (+1.94)
      - acousticness 0.89 is 0.09 from target (+0.91)

============================================================
```

Worked best. All 5 are quiet songs, and mood beat genre for Spacewalk Thoughts.

### Deep Intense Rock (Normal)

```
============================================================
  PROFILE: Deep Intense Rock
  rock / intense / energy 0.92 / likes acoustic: False
============================================================

#1  Storm Runner by Voltline
    Genre: rock  |  Mood: intense
    Score: 5.88
    Why:
      - mood match (+2.0)
      - genre match (+1.0)
      - energy 0.91 is 0.01 from target (+1.98)
      - acousticness 0.10 is 0.10 from target (+0.90)

#2  Gym Hero by Max Pulse
    Genre: pop  |  Mood: intense
    Score: 4.83
    Why:
      - mood match (+2.0)
      - energy 0.93 is 0.01 from target (+1.98)
      - acousticness 0.05 is 0.15 from target (+0.85)

#3  Sunrise City by Neon Echo
    Genre: pop  |  Mood: happy
    Score: 2.78
    Why:
      - energy 0.82 is 0.10 from target (+1.80)
      - acousticness 0.18 is 0.02 from target (+0.98)

#4  Neon Pulse by Circuit Haze
    Genre: edm  |  Mood: energetic
    Score: 2.77
    Why:
      - energy 0.95 is 0.03 from target (+1.94)
      - acousticness 0.03 is 0.17 from target (+0.83)

#5  Iron Tide by Black Anvil
    Genre: metal  |  Mood: angry
    Score: 2.74
    Why:
      - energy 0.97 is 0.05 from target (+1.90)
      - acousticness 0.04 is 0.16 from target (+0.84)

============================================================
```

Storm Runner is first like it should be. After #2 it's only energy, so happy and angry songs get mixed together.

### Conflicted (sad but wants high energy) (Adversarial)

```
============================================================
  PROFILE: Conflicted (sad but wants high energy)
  classical / melancholy / energy 0.9 / likes acoustic: False
============================================================

#1  Hollow Winter by Clara Voss
    Genre: classical  |  Mood: melancholy
    Score: 3.79
    Why:
      - mood match (+2.0)
      - genre match (+1.0)
      - energy 0.18 is 0.72 from target (+0.56)
      - acousticness 0.97 is 0.77 from target (+0.23)

#2  Storm Runner by Voltline
    Genre: rock  |  Mood: intense
    Score: 2.88
    Why:
      - energy 0.91 is 0.01 from target (+1.98)
      - acousticness 0.10 is 0.10 from target (+0.90)

#3  Sunrise City by Neon Echo
    Genre: pop  |  Mood: happy
    Score: 2.82
    Why:
      - energy 0.82 is 0.08 from target (+1.84)
      - acousticness 0.18 is 0.02 from target (+0.98)

#4  Gym Hero by Max Pulse
    Genre: pop  |  Mood: intense
    Score: 2.79
    Why:
      - energy 0.93 is 0.03 from target (+1.94)
      - acousticness 0.05 is 0.15 from target (+0.85)

#5  Neon Pulse by Circuit Haze
    Genre: edm  |  Mood: energetic
    Score: 2.73
    Why:
      - energy 0.95 is 0.05 from target (+1.90)
      - acousticness 0.03 is 0.17 from target (+0.83)

============================================================
```

This tricked it. Hollow Winter has energy 0.18 but is still #1 because the labels give it 3 points. The labels beat the numbers.

### Unknown labels (genre/mood not in catalog) (Adversarial)

```
============================================================
  PROFILE: Unknown labels (genre/mood not in catalog)
  k-pop / euphoric / energy 0.7 / likes acoustic: False
============================================================

#1  Night Drive Loop by Neon Echo
    Genre: synthwave  |  Mood: moody
    Score: 2.88
    Why:
      - energy 0.75 is 0.05 from target (+1.90)
      - acousticness 0.22 is 0.02 from target (+0.98)

#2  Concrete Jungle by Kid Cipher
    Genre: hip hop  |  Mood: confident
    Score: 2.76
    Why:
      - energy 0.78 is 0.08 from target (+1.84)
      - acousticness 0.12 is 0.08 from target (+0.92)

#3  Sunrise City by Neon Echo
    Genre: pop  |  Mood: happy
    Score: 2.74
    Why:
      - energy 0.82 is 0.12 from target (+1.76)
      - acousticness 0.18 is 0.02 from target (+0.98)

#4  Rooftop Lights by Indigo Parade
    Genre: indie pop  |  Mood: happy
    Score: 2.73
    Why:
      - energy 0.76 is 0.06 from target (+1.88)
      - acousticness 0.35 is 0.15 from target (+0.85)

#5  Island Breeze by Sol Marley
    Genre: reggae  |  Mood: uplifting
    Score: 2.55
    Why:
      - energy 0.60 is 0.10 from target (+1.80)
      - acousticness 0.45 is 0.25 from target (+0.75)

============================================================
```

Nothing matched, so the scores are all close and it only uses energy. It never says nothing really matched.

### Acoustic metal (acoustic taste vs. loud genre) (Adversarial)

```
============================================================
  PROFILE: Acoustic metal (acoustic taste vs. loud genre)
  metal / angry / energy 0.97 / likes acoustic: True
============================================================

#1  Iron Tide by Black Anvil
    Genre: metal  |  Mood: angry
    Score: 5.24
    Why:
      - mood match (+2.0)
      - genre match (+1.0)
      - energy 0.97 is 0.00 from target (+2.00)
      - acousticness 0.04 is 0.76 from target (+0.24)

#2  Neon Pulse by Circuit Haze
    Genre: edm  |  Mood: energetic
    Score: 2.19
    Why:
      - energy 0.95 is 0.02 from target (+1.96)
      - acousticness 0.03 is 0.77 from target (+0.23)

#3  Storm Runner by Voltline
    Genre: rock  |  Mood: intense
    Score: 2.18
    Why:
      - energy 0.91 is 0.06 from target (+1.88)
      - acousticness 0.10 is 0.70 from target (+0.30)

#4  Gym Hero by Max Pulse
    Genre: pop  |  Mood: intense
    Score: 2.17
    Why:
      - energy 0.93 is 0.04 from target (+1.92)
      - acousticness 0.05 is 0.75 from target (+0.25)

#5  Rooftop Lights by Indigo Parade
    Genre: indie pop  |  Mood: happy
    Score: 2.13
    Why:
      - energy 0.76 is 0.21 from target (+1.58)
      - acousticness 0.35 is 0.45 from target (+0.55)

============================================================
```

Iron Tide is #1 even though it's not acoustic, because acousticness is only worth 1 point.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



