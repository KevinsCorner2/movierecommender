import pandas as pd

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
