# AI Interactions Log

---

## Agentic Workflow (SF8)

**What task did you give the agent?**

I asked the agent to add 5 new song features to the dataset and make the scoring use them. I also asked for scoring modes, a diversity penalty, and a summary table for the output. All of it was done on a separate branch (`experiment/advanced-challenges`) so `main` stayed safe.

**Prompts used:**

- "Introduce 5 or more attributes that aren't in the baseline data (like popularity, release decade, detailed mood tags). Update data/songs.csv and the scoring logic in src/recommender.py so scoring accounts for them."
- "Build two or more ranking strategies so I can switch modes in main.py. Brainstorm a simple design pattern that keeps the code modular."
- "Add a diversity penalty that lowers a song's score if its artist (or genre) is already in the top recommendations."
- "Show the top recommendations as a formatted table that includes the reasons for each score."

**What did the agent generate or change?**

- `data/songs.csv`: added 5 columns to all 18 songs: `popularity` (0-100), `release_decade`, `mood_tags` (like `nostalgic|warm`), `instrumentalness`, and `speechiness`. The agent made up the values.
- `src/recommender.py`:
  - `load_songs` converts the new columns (and splits the tags into a list).
  - `score_song` now scores tags, popularity, decade, instrumentalness, and speechiness. Each one only counts if the user profile asks for it.
  - A `ScoringMode` class with 4 modes (`balanced`, `genre_first`, `mood_first`, `energy_focused`).
  - `recommend_songs` takes `mode` and `diversity` options. With diversity on, it picks songs one at a time and takes points off a song for each artist (-1.0) or genre (-0.5) already picked, and adds the penalty to the reasons.
- `src/main.py`: command line options `--mode`, `--diversity`, and `--table`, a new "Nostalgic 90s Acoustic" profile that uses the new features, and a `format_table` function that prints an ASCII table with the reasons for each song.

**What did you verify or fix manually?**

- Ran the old and new code side by side on my 6 original profiles. The results, scores, and reasons were identical, so the new features didn't break anything. The 2 tests in `tests/test_recommender.py` still pass.
- Checked one score by hand. Dusty Porch for the new profile: 2.0 + 1.0 + 1.94 + 1.0 + 1.5 + 0.49 + 0.5 + 0.5 = 8.93, which matches the output.
- Checked that the diversity penalty works. Gym Hero for High-Energy Pop goes from 3.79 to 3.29 (-0.5 for a second pop song), and for the Unknown labels profile the second Neon Echo song (Sunrise City) gets dropped and Paper Hearts takes its spot.
- The numbers for the new features are invented, not real data, so rankings that use them are only for demo purposes.
- I left the `Song` dataclass alone because the tests use it. The new features only exist in the dictionaries from `load_songs`.
- I didn't use the `tabulate` library. Plain text formatting works and doesn't add a dependency.

---

## Design Pattern (SF10)

**Which design pattern did you use?**

A simple Strategy pattern. The scoring function stays the same, and each "mode" is a small object that only holds the weights.

**How did AI help you brainstorm or implement it?**

I asked for a way to switch between ranking styles without copying the scoring code. The options were:
1. A separate scoring function for each mode.
2. A class for each mode.
3. One scoring function plus a table of weights per mode.

I went with option 3 because the modes only differ in how many points each rule is worth, so there is no reason to repeat the logic. It also means adding a new mode is one extra line. The AI wrote the code. I picked the approach and checked that the default mode gives the same results as before.

**How does the pattern appear in your final code?**

- `ScoringMode` in `src/recommender.py` is the strategy. It holds the weights.
- `SCORING_MODES` is the list of available modes.
- `score_song(user_prefs, song, mode)` is the one scoring function. It reads its weights from whichever mode it's given.
- `main.py --mode mood_first` (or `genre_first`, `energy_focused`, `all`) switches the strategy from the command line.
