# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
