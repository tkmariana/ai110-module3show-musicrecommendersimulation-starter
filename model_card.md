# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**  

---

## 2. Intended Use  

**Goal:** suggest the top 5 songs from a small list that best fit what a user likes. It looks at genre, mood, energy, and how acoustic a song is.

**Assumptions:** the user knows their favorite genre and mood, and has one clear taste.

**Intended use:** classroom practice and learning how recommenders work.

**Not intended for:** real users, real music apps, or deciding what someone's taste should be. The song list is too small and I made up some of the numbers.

---

## 3. How the Model Works  

My recommender looks at every song in the catalog one at a time and gives it a score based on how well it fits what the user likes. Then it puts the songs in order from highest score to lowest and shows the top 5.

**What it looks at:** for each song it uses the genre, the mood, how energetic it is, and how acoustic it is. The user tells it their favorite genre, their favorite mood, how much energy they want, and whether they like acoustic music or not.

**How the score works:** a song can earn up to 6 points.
- 2 points if the mood is the one the user wants
- 1 point if the genre is the one the user wants
- up to 2 points for energy, and the closer the song is to the energy the user wants, the more points it gets
- up to 1 point for acousticness, based on how close it is to what the user likes

The important part is that energy is about being close, not about being high. If someone wants calm music, a quiet song gets more points than a loud one, and if they want intense music it's the other way around.

**Why this way:** I made mood worth more than genre because the genres in my catalog mostly show up only once, so a genre match doesn't say much, while mood usually lines up with how a song actually feels. If two songs end up with the same score, the one with closer energy goes first. Each recommendation also comes with the reasons for its score, so you can see why it was picked.

**What I changed from the starter:** the starter code didn't have any scoring or ranking, so I wrote the part that loads the songs, the part that scores one song, and the part that ranks all of them. I also added 8 more songs to the starter list so there's more variety.

---

## 4. Data  

There are 18 songs. The starter had 10 and I added 8 with new genres and moods. Each song has a genre, mood, energy, tempo, valence, danceability, and acousticness. I only use genre, mood, energy, and acousticness.

**Limits:**
- It's small. There are 15 genres and 14 moods, so most show up only once.
- Energy is lopsided: 9 songs are low, 8 are high, and only 1 is in the middle.
- The numbers for my 8 new songs are made up.
- It has nothing about lyrics, language, or what's popular.

---

## 5. Strengths  

It works best when the user's genre, mood, and energy all agree. Chill Lofi got 5 quiet, acoustic songs, and Rock got Storm Runner first, which is what I expected. Energy works well because it rewards songs that are close, not just high. The reasons also make it easy to see why each song was picked.

---

## 6. Limitations and Bias 

The biggest weakness I found is that the mood and genre labels can beat the numbers. When I tested a user who likes classical and melancholy music but wants energy 0.9, the system still put Hollow Winter first, even though its energy is only 0.18. It got there because a mood match and a genre match give it 3 free points, which is more than a song can lose by being far from the target energy. I also noticed that most of my moods only show up on one song, so a lot of users can only get a mood match for a single song. This means the system listens to what people call their taste more than what they actually asked for in the numbers.

---

## 7. Evaluation  

I tested 6 profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and 3 tricky ones I made up (Conflicted, Unknown labels, Acoustic metal). I checked if the top 5 felt right and if the reasons made sense.

**What surprised me:** Gym Hero kept showing up, the Conflicted user got a really quiet song as #1, and the Unknown labels user still got 5 normal-looking results even though nothing matched.

**Comparing profiles:**
- **Pop vs. Lofi:** no songs in common. Pop wants loud songs and Lofi wants quiet acoustic ones, which makes sense.
- **Pop vs. Rock:** 4 of 5 songs are the same since they both want high energy. Only #1 is different because of the mood and genre match.
- **Rock vs. Lofi:** no overlap, opposite energy and acoustic taste.
- **Conflicted vs. Rock:** #2 to #5 are the same loud songs, but Conflicted gets Hollow Winter at #1 just from the labels. That's the weak spot.
- **Unknown labels vs. Pop:** both want fairly high energy, but with no label matches the scores are much lower (2.88 vs. 5.82). That makes sense since nothing really fit.
- **Acoustic metal vs. Rock:** same loud songs, and liking acoustic barely changed anything because it's only worth 1 point.

**Why Gym Hero shows up for Happy Pop:** think of the system like a teacher grading a checklist. The person asked for pop, happy, and high energy. Gym Hero is pop and it's very high energy, so it gets points for two of the three things. It only misses on "happy," because it's a workout song. There are only 2 happy songs in my list, and after those, Gym Hero is the closest one left. The system just counts points, so it can't tell that a pumped-up gym song feels different from a feel-good song.

---

## 8. Future Work  

- Score valence too, so a happy song and an angry song don't look the same.
- Give partial credit for close moods, like "chill" and "relaxed."
- Add more songs, and show a warning when nothing really matches the user.

---

## 9. Personal Reflection  

My biggest learning moment was seeing how much a few weights decide. When I tested a user who wanted high energy but liked classical and melancholy, a quiet song still came first because the labels gave it more points than the energy took away.

AI helped me write the code and come up with tricky profiles to test. But I had to double-check it. I checked the scores by hand, and when we changed the weights, it wasn't clear the new results were actually better, just different.

What surprised me is that simply adding up points already feels like a real recommendation. The output looks smart even though it's just counting.

Next I would add valence, partial credit for close moods, and more songs.
