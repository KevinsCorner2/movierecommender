import requests
from random import choice

# TMDB API setup
API_KEY = "930f22a3bf4568399047e03b09bb94aa"
BASE_URL = "https://api.themoviedb.org/3"


def search_movie(title):
    """
    Search for a movie by title using the TMDB API.

    Args:
        title (str): The name of the movie to search for.

    Returns:
        dict: A dictionary containing movie details if found, otherwise None.
    """
    try:
        url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={title}"
        response = requests.get(url).json()

        if response.get("results"):
            movie = response["results"][0]  # Select the first result
            return {
                "id": movie["id"],
                "title": movie["title"],
                "year": movie.get("release_date", "Unknown")[:4],
                "rating": f"{movie.get('vote_average', 0) * 10:.0f}%",
                "overview": movie.get("overview", "No overview available."),
                "poster_path": (
                    f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                    if movie.get("poster_path") else None
                ),
                "watch_providers": get_watch_providers(movie["id"]),
                "cast": get_movie_cast(movie["id"]),
            }
    except Exception as e:
        print(f"Error fetching movie: {e}")
    
    return None


def get_similar_movies(movie_id):
    """
    Retrieve similar movie recommendations from TMDB.

    Args:
        movie_id (int): The TMDB ID of the movie.

    Returns:
        list: A list of up to 5 similar movies, each represented as a dictionary.
    """
    try:
        url = f"{BASE_URL}/movie/{movie_id}/similar?api_key={API_KEY}"
        response = requests.get(url).json()

        movies = []
        for movie in response.get("results", [])[:5]:  # Limit to 5 recommendations
            movies.append({
                "title": movie["title"],
                "year": movie.get("release_date", "Unknown")[:4],
                "rating": f"{movie.get('vote_average', 0) * 10:.0f}%",
                "poster_path": (
                    f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                    if movie.get("poster_path") else None
                )
            })
        return movies
    except Exception as e:
        print(f"Error fetching similar movies: {e}")
    
    return []


def get_random_movie():
    """
    Fetch a random highly-rated movie from TMDB.

    Returns:
        dict: A dictionary containing details about the randomly selected movie.
    """
    try:
        url = f"{BASE_URL}/movie/popular?api_key={API_KEY}"
        response = requests.get(url).json()

        if response.get("results"):
            movie = choice(response["results"])  # Select a random movie
            return {
                "id": movie["id"],
                "title": movie["title"],
                "year": movie.get("release_date", "Unknown")[:4],
                "rating": f"{movie.get('vote_average', 0) * 10:.0f}%",
                "overview": movie.get("overview", "No overview available."),
                "poster_path": (
                    f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                    if movie.get("poster_path") else None
                ),
                "watch_providers": get_watch_providers(movie["id"]),
                "cast": get_movie_cast(movie["id"]),
            }
    except Exception as e:
        print(f"Error fetching random movie: {e}")
    
    return None


def get_watch_providers(movie_id):
    """
    Get available streaming, rental, and purchase options for a movie.

    Args:
        movie_id (int): The TMDB ID of the movie.

    Returns:
        dict: A dictionary containing streaming, rent, and buy options.
    """
    try:
        url = f"{BASE_URL}/movie/{movie_id}/watch/providers?api_key={API_KEY}"
        response = requests.get(url).json()

        # Assuming US-based results
        providers = response.get("results", {}).get("US", {})

        return {
            "streaming": [p["provider_name"] for p in providers.get("flatrate", [])],
            "rent": [p["provider_name"] for p in providers.get("rent", [])],
            "buy": [p["provider_name"] for p in providers.get("buy", [])],
        }
    except Exception as e:
        print(f"Error fetching watch providers: {e}")
    
    return {"streaming": [], "rent": [], "buy": []}


def get_movie_cast(movie_id):
    """
    Retrieve the top-billed cast members and their profile pictures.

    Args:
        movie_id (int): The TMDB ID of the movie.

    Returns:
        list: A list of up to 5 top-billed cast members.
    """
    try:
        url = f"{BASE_URL}/movie/{movie_id}/credits?api_key={API_KEY}"
        response = requests.get(url).json()

        cast_list = []
        for actor in response.get("cast", [])[:5]:  # Limit to top 5 cast members
            cast_list.append({
                "name": actor["name"],
                "character": actor.get("character", "Unknown"),
                "profile_pic": (
                    f"https://image.tmdb.org/t/p/w200{actor['profile_path']}"
                    if actor.get("profile_path") else None
                )
            })
        return cast_list
    except Exception as e:
        print(f"Error fetching movie cast: {e}")
    
    return []


def get_movies_by_genre(genre):
    """
    Fetch movies based on the selected genre.

    Args:
        genre (str): The genre name.

    Returns:
        list: A list of movies within the specified genre.
    """
    genre_dict = {
        "Action": 28,
        "Adventure": 12,
        "Animation": 16,
        "Comedy": 35,
        "Crime": 80,
        "Documentary": 99,
        "Drama": 18,
        "Family": 10751,
        "Fantasy": 14,
        "History": 36,
        "Horror": 27,
        "Music": 10402,
        "Mystery": 9648,
        "Romance": 10749,
        "Science Fiction": 878,
        "Thriller": 53,
        "TV Movie": 10770,
        "War": 10752,
        "Western": 37,
    }

    genre_id = genre_dict.get(genre)
    if not genre_id:
        return []

    try:
        url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&with_genres={genre_id}"
        response = requests.get(url).json()

        movies = []
        for movie in response.get("results", []):
            movies.append({
                "title": movie["title"],
                "year": (
                    movie["release_date"][:4] if "release_date" in movie else "Unknown"
                ),
                "rating": (
                    f"{movie['vote_average'] * 10:.0f}%" if movie.get("vote_average")
                    else "N/A"
                ),
                "overview": movie.get("overview", "No description available."),
                "poster_path": (
                    f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                    if movie.get("poster_path") else None
                )
            })
        return movies
    except Exception as e:
        print(f"Error fetching movies by genre: {e}")
    
    return []
