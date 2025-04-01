
import requests

API_KEY = "930f22a3bf4568399047e03b09bb94aa"
BASE_URL = "https://api.themoviedb.org/3"

def search_movie(title):
    """Search for a movie by title using the TMDB API."""
    url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={title}"
    response = requests.get(url).json()
    return response["results"][0] if response["results"] else None

def get_similar_movies(movie_id):
    """Get similar movie recommendations from TMDB."""
    url = f"{BASE_URL}/movie/{movie_id}/similar?api_key={API_KEY}"
    response = requests.get(url).json()
    return response["results"][:5] if response["results"] else []

def get_random_movie():
    """Fetch a random highly-rated movie."""
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}"
    response = requests.get(url).json()
    from random import choice
    return choice(response["results"]) if response["results"] else None




