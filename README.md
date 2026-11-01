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



