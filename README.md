This project contains a website for a movie recommender using streamlit as a host. Using TMDB, the goal is to gather data on what movies are avaliable, and allow the user to explore movie options based in four catigories. First being a search directly for the movie, second, a movie search by similarity to personal favorites, third being a search by genre, and finally a random search to generate diversity in movie selection.
in these being In this repository, the user will find a few codes. 

Breakdown of codes

app.py 
-  main landing page when you log into your website, gives you 4 pages.
-    tab 1: movie search
-    tab 2: personalized search
-    tab 3: search by genre
-    tab 4: randomized movie generator

movie_recommender.py
- contains list of def for use in either tmdb_api and app.py

tmdb_api.py
- uses requests from The movie database, and contains an API key.

movies.csv
- code used to pull from a spread sheet, but since updating to pull from the database itself, its no longer used, but still avaliable for those who want to use this code.
