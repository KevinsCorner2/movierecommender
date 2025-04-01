import pandas as pd
import random

class MovieRecommender:
    """
    A movie recommendation system that allows users to:
    - Recommend movies based on genre.
    - Rate movies.
    - Retrieve top-rated movies by the user.
    """
    
    def __init__(self, data_path="movies.csv"):
        """Initialize the movie recommender by loading the dataset."""
        self.movies = pd.read_csv(data_path)  # Load movie data from CSV file
        self.user_ratings = {}  # Dictionary to store user ratings dynamically

    def recommend_by_genre(self, genre):
        """
        Recommend top 5 movies matching the given genre.
        
        Args:
            genre (str): The genre to filter movies by.
        
        Returns:
            DataFrame: Top 5 movies sorted by rating, containing title, year, rating, and description.
        """
        # Filter movies that contain the given genre (case insensitive)
        filtered_movies = self.movies[
            self.movies["genre"].str.contains(genre, case=False, na=False)
        ]
        # Return top 5 movies based on rating
        return filtered_movies.nlargest(5, "rating")[
            ["title", "year", "rating", "description"]
        ]

    def rate_movie(self, title, rating):
        """
        Allow users to rate a movie.
        
        Args:
            title (str): The title of the movie.
            rating (float): The user's rating for the movie (out of 5).
        
        Returns:
            str: Confirmation message including the rating.
        """
        self.user_ratings[title] = rating  # Store the rating
        return f"You rated '{title}' {rating}/5 ⭐"

    def get_top_rated(self):
        """
        Recommend movies based on user's highest-rated choices.
        
        Returns:
            list: Top 3 highest-rated movies by the user.
            str: A message if no ratings are available.
        """
        if not self.user_ratings:
            return "No ratings yet! Rate some movies first."
        
        # Sort movies by rating in descending order and return the top 3
        top_movies = sorted(
            self.user_ratings.items(), key=lambda x: x[1], reverse=True
        )[:3]
        return [m[0] for m in top_movies]

def get_random_movie(self):
    """
    Return a random movie from the dataset, including cast information.
    
    Returns:
        dict: A dictionary containing details about the random movie.
    """
    # Randomly select one movie from the dataset
    random_movie = self.movies.sample(n=1).iloc[0]  

    # Parse cast names and their images (assuming they are comma-separated)
    cast = random_movie["cast"].split(",")  
    cast_images = random_movie["cast_images"].split(",")  

    return {
        "title": random_movie["title"],
        "year": random_movie["year"],
        "rating": random_movie["rating"],
        "description": random_movie["description"],
        "poster_path": random_movie["poster_path"],
        "streaming_service": random_movie["streaming_service"],
        "availability": random_movie["availability"],
        "cast": cast,
        "cast_images": cast_images
    }
