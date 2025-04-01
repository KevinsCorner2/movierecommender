import pandas as pd
import random

class MovieRecommender:
    def __init__(self, data_path="movies.csv"):
        """Load movie dataset."""
        self.movies = pd.read_csv(data_path)
        self.user_ratings = {}  # Store user ratings dynamically

    def recommend_by_genre(self, genre):
        """Return top 5 movies matching the given genre."""
        filtered_movies = self.movies[self.movies["genre"].str.contains(genre, case=False, na=False)]
        return filtered_movies.nlargest(5, "rating")[["title", "year", "rating", "description"]]

    def rate_movie(self, title, rating):
        """Allow users to rate a movie."""
        self.user_ratings[title] = rating
        return f"You rated '{title}' {rating}/5 ⭐"

    def get_top_rated(self):
        """Recommend movies based on user's highest-rated choices."""
        if not self.user_ratings:
            return "No ratings yet! Rate some movies first."
        top_movies = sorted(self.user_ratings.items(), key=lambda x: x[1], reverse=True)[:3]
        return [m[0] for m in top_movies]

def get_random_movie(self):
    """Return a random movie from the dataset, including cast information."""
    random_movie = self.movies.sample(n=1).iloc[0]  # Get a random movie from the dataset
    cast = random_movie["cast"].split(",")  # Assuming cast names are comma-separated
    cast_images = random_movie["cast_images"].split(",")  # Assuming cast images are comma-separated URLs
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
