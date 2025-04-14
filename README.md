This project contains a website for a movie recommender using Streamlit as a host. Using TMDB, the goal is to gather data on what movies are available and allow the user to explore movie options based on four categories. First, a search directly for the movie; second, a movie search by similarity to personal favorites; third, a search by genre; and finally, a random search to generate diversity in the  movie selection.
in these being In this repository, the user will find a few codes. 

Breakdown of codes

app.py 
-  The main landing page, when you log into your website, gives you 4 pages.
-    tab 1: movie search
-    tab 2: personalized search
-    tab 3: search by genre
-    tab 4: randomized movie generator

movie_recommender.py
- contains list of def for use in either tmdb_api and app.py

tmdb_api.py
- It uses requests from the movie database and contains an API key.

movies.csv
- The code used to pull from a spreadsheet, but since updating to pull from the database itself, it's no longer used but is still available for those who want to use this code.

to run: clone the repository and once you have opened your terminal, type "python -m streamlit run app.py"


https://movierecomende.streamlit.app/
