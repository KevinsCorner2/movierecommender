import streamlit as st
from movie_recommender import MovieRecommender
from tmdb_api import search_movie, get_similar_movies, get_random_movie, get_movies_by_genre

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
            col1, col2 = st.columns([1, 2])
            with col1:
                if movie.get("poster_path"):
                    st.image(movie["poster_path"])
                else:
                    st.write("No poster available.")
            
            with col2:
                st.write(f"🎬 **{movie['title']} ({movie.get('year', 'Unknown')})**")
                st.write(f"⭐ Rating: {movie.get('rating', 'N/A')}%")
                st.write(movie.get("overview", "No description available."))

                # Watch Providers
                watch_providers = movie.get("watch_providers", {})
                if watch_providers and any(watch_providers.values()):
                    st.subheader("Where to Watch:")
                    if watch_providers["streaming"]:
                        st.write(f"📺 **Streaming:** {', '.join(watch_providers['streaming'])}")
                    if watch_providers["rent"]:
                        st.write(f"💰 **Rent:** {', '.join(watch_providers['rent'])}")
                    if watch_providers["buy"]:
                        st.write(f"🛒 **Buy:** {', '.join(watch_providers['buy'])}")
                else:
                    st.write("No watch providers available.")

            # 🎭 Display Top Billed Cast - Carousel
            cast = movie.get("cast", [])
            if cast:
                st.subheader("🎭 Top Billed Cast:")
                num_columns = min(5, len(cast))
                cols = st.columns(num_columns)
                for i, actor in enumerate(cast[:num_columns]):
                    with cols[i]:
                        if actor.get("profile_pic"):
                            st.image(actor["profile_pic"], width=100)
                        st.write(f"**{actor['name']}**")
                        st.caption(f"as {actor['character']}")

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
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if rec.get("poster_path"):
                            st.image(rec["poster_path"])
                        else:
                            st.write("No poster available.")
                    with col2:
                        st.write(f"🎬 **{rec['title']} ({rec.get('year', 'Unknown')})** - ⭐ {rec.get('rating', 'N/A')}%")
            else:
                st.write("No similar movies found.")
        else:
            st.write("Movie not found.")

# 🎥 Genre-Based Recommendations
with tab3:
    st.subheader("Recommend Movies by Genre")
    genre = st.selectbox("Select a Genre", [
        "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
        "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
        "Romance", "Science Fiction", "Thriller", "TV Movie", "War", "Western"
    ])
    if st.button("Get Genre Recommendations"):
        movies = get_movies_by_genre(genre)
        if movies:
            for movie in movies:
                col1, col2 = st.columns([1, 3])
                with col1:
                    if movie.get("poster_path"):
                        st.image(movie["poster_path"])
                    else:
                        st.write("No poster available.")
                with col2:
                    st.write(f"🎬 **{movie['title']} ({movie.get('year', 'Unknown')})** - ⭐ {movie.get('rating', 'N/A')}%")
                    st.write(movie.get("overview", "No description available."))
        else:
            st.write("No movies found for this genre.")

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
            col1, col2 = st.columns([1, 2])
            with col1:
                if movie.get("poster_path"):
                    st.image(movie["poster_path"])
                else:
                    st.write("No poster available.")
            
            with col2:
                st.write(f"🎬 **{movie['title']} ({movie.get('year', 'Unknown')})** - ⭐ {movie.get('rating', 'N/A')}%")
                st.write(movie.get("overview", "No description available."))

                # Watch Providers
                watch_providers = movie.get("watch_providers", {})
                if watch_providers and any(watch_providers.values()):
                    st.subheader("Where to Watch:")
                    if watch_providers["streaming"]:
                        st.write(f"📺 **Streaming:** {', '.join(watch_providers['streaming'])}")
                    if watch_providers["rent"]:
                        st.write(f"💰 **Rent:** {', '.join(watch_providers['rent'])}")
                    if watch_providers["buy"]:
                        st.write(f"🛒 **Buy:** {', '.join(watch_providers['buy'])}")
                else:
                    st.write("No watch providers available.")

            # 🎭 Display Top Billed Cast - Carousel
            cast = movie.get("cast", [])
            if cast:
                st.subheader("🎭 Top Billed Cast:")
                num_columns = min(5, len(cast))
                cols = st.columns(num_columns)
                for i, actor in enumerate(cast[:num_columns]):
                    with cols[i]:
                        if actor.get("profile_pic"):
                            st.image(actor["profile_pic"], width=100)
                        st.write(f"**{actor['name']}**")
                        st.caption(f"as {actor['character']}")

        else:
            st.write("Couldn't fetch a random movie.")
