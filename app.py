import streamlit as st
from movie_recommender import MovieRecommender
from tmdb_api import search_movie, get_similar_movies, get_random_movie

st.title("🎬 Smart Movie Recommender")

# Initialize movie recommender
recommender = MovieRecommender()

# Tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 Search", "🎭 Personalized", "🎥 Genre", "⭐ Ratings", "🎲 Surprise Me"])

# 🔍 Movie Search
with tab1:
    st.subheader("Search for a Movie")
    movie_name = st.text_input("Enter a movie name")
    if st.button("Search"):
        movie = search_movie(movie_name)
        if movie:
            # Display movie poster
            st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")
            
            # Movie title and release year
            st.write(f"**{movie['title']} ({movie['release_date'][:4]})**")
            
            # Rating (converted to percentage)
            rating_percentage = movie['vote_average'] * 10  # Convert to percentage
            st.write(f"⭐ Rating: {rating_percentage}%")

            # Overview of the movie
            st.write(movie["overview"])

            # Display the availability (rent, buy, streaming service)
            st.write(f"**Available for:** {movie.get('availability', 'Information not available')}")
            
            # Display the streaming service if available
            st.write(f"**Streaming on:** {movie.get('streaming_service', 'Information not available')}")

            # Display the top-billed cast
            if 'cast' in movie and 'cast_images' in movie:
                st.subheader("Top Billed Cast:")
                for actor, image in zip(movie['cast'], movie['cast_images']):
                    st.write(f"{actor} - ![Actor Image](https://image.tmdb.org/t/p/w500{image})")

        else:
            st.write("Movie not found.")


# 🎭 Personalized Recommendations
with tab2:
    st.subheader("Get Recommendations Based on Your Favorite Movie")
    favorite_movie = st.text_input("Enter a favorite movie")
    if st.button("Recommend Similar"):
        movie = search_movie(favorite_movie)
        if movie:
            recommendations = get_similar_movies(movie["id"])
            if recommendations:
                for rec in recommendations:
                    st.write(f"🎬 {rec['title']} ({rec['release_date'][:4]}) - ⭐ {rec['vote_average']}")
            else:
                st.write("No similar movies found.")
        else:
            st.write("Movie not found.")

# 🎥 Genre-Based Recommendations
with tab3:
    st.subheader("Recommend Movies by Genre")
    genre = st.selectbox("Select a Genre", ["Sci-Fi", "Action", "Romance", "Thriller"])
    if st.button("Get Genre Recommendations"):
        movies = recommender.recommend_by_genre(genre)
        for _, row in movies.iterrows():
            st.write(f"🎬 **{row['title']} ({row['year']})** - ⭐ {row['rating']}")
            st.write(row["description"])

# ⭐ User Ratings & Reviews
with tab4:
    st.subheader("Rate a Movie")
    movie_to_rate = st.text_input("Enter a movie title to rate")
    rating = st.slider("Select Rating", 1, 5, 3)
    if st.button("Submit Rating"):
        st.write(recommender.rate_movie(movie_to_rate, rating))

    st.subheader("Your Top Rated Movies")
    st.write(recommender.get_top_rated())

# 🎲 Surprise Me!
with tab5:
    st.subheader("Surprise Me with a Random Movie!")
    if st.button("Give me a movie!"):
        movie = get_random_movie()
        if movie:
            # Convert vote average to percentage
            vote_percentage = movie['vote_average'] * 10  # Convert to percentage (0-100)
            
            # Display movie details
            st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")
            st.write(f"🎬 **{movie['title']} ({movie['release_date'][:4]})** - ⭐ {vote_percentage:.1f}%")
            st.write(movie["overview"])
            
            # Display Watch Providers (Stream, Buy, Rent)
            if movie.get("watch_providers"):
                providers = movie["watch_providers"].get("US", {})
                streaming = providers.get("flatrate", [])
                rent = providers.get("rent", [])
                buy = providers.get("buy", [])
                
                st.write("🔮 Available on:")
                
                if streaming:
                    st.write("**Streaming:**")
                    for provider in streaming:
                        st.write(f"- {provider['provider_name']}")
                if rent:
                    st.write("**Available to Rent:**")
                    for provider in rent:
                        st.write(f"- {provider['provider_name']}")
                if buy:
                    st.write("**Available to Buy:**")
                    for provider in buy:
                        st.write(f"- {provider['provider_name']}")
            
            # Display Top-Billed Cast
            if movie.get("cast"):
                st.write("👨‍👩‍👧‍👦 Top Cast:")
                for cast_member in movie["cast"]:
                    st.image(f"https://image.tmdb.org/t/p/w500{cast_member['profile_path']}", width=50)
                    st.write(f"**{cast_member['name']}** as {cast_member['character']}")
        else:
            st.write("Couldn't fetch a random movie.")

