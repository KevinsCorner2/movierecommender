import streamlit as st
from movie_recommender import MovieRecommender
from tmdb_api import search_movie, get_similar_movies, get_random_movie, get_movies_by_genre

# Inject custom CSS for fancy fonts and layout styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        background-color: #0f1117;
        color: #e5e5e5;
    }

    h1, h2, h3, h4 {
        color: #f9a825;
    }

    .stButton>button {
        background-color: #f9a825;
        color: black;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1em;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #ffd54f;
        color: black;
        transform: scale(1.05);
    }

    .stImage>img {
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: transform 0.2s ease;
    }

    .stImage>img:hover {
        transform: scale(1.03);
    }

    .stTabs [role="tab"] {
        font-size: 18px;
        font-weight: bold;
    }

    .stSelectbox, .stTextInput {
        background-color: #1c1f26 !important;
        color: #e5e5e5 !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommender")

# Initialize movie recommender
recommender = MovieRecommender()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Search", "🎭 Personalized", "🎥 Genre", "🎲 Surprise Me"])

# 🔍 Search
with tab1:
    st.header("🔎 Search for a Movie")
    movie_name = st.text_input("Type a movie title...")

    if st.button("Search"):
        movie = search_movie(movie_name)
        if movie:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(movie.get("poster_path", ""), use_container_width=True)
            with col2:
                st.markdown(f"### 🎬 {movie['title']} ({movie.get('year', 'Unknown')})")
                st.write(f"⭐ **Rating:** {movie.get('rating', 'N/A')}")
                st.write(movie.get("overview", "No description available."))

                watch = movie.get("watch_providers", {})
                if watch and any(watch.values()):
                    st.markdown("**📍 Where to Watch:**")
                    if watch.get("streaming"):
                        st.write(f"📺 Streaming: {', '.join(watch['streaming'])}")
                    if watch.get("rent"):
                        st.write(f"💰 Rent: {', '.join(watch['rent'])}")
                    if watch.get("buy"):
                        st.write(f"🛒 Buy: {', '.join(watch['buy'])}")
                else:
                    st.write("No watch providers available.")

            cast = movie.get("cast", [])
            if cast:
                st.subheader("🎭 Top Billed Cast")
                cols = st.columns(min(5, len(cast)))
                for i, actor in enumerate(cast[:5]):
                    with cols[i]:
                        st.image(actor.get("profile_pic", ""), width=100)
                        st.write(f"**{actor['name']}**")
                        st.caption(f"as {actor['character']}")
        else:
            st.warning("🚫 Movie not found.")

# 🎭 Personalized Recommendations
with tab2:
    st.header("💡 Get Recommendations from a Favorite")
    favorite_movie = st.text_input("What's a movie you love?")

    if st.button("Recommend Similar"):
        movie = search_movie(favorite_movie)
        if movie:
            recommendations = get_similar_movies(movie["id"])
            if recommendations:
                for rec in recommendations:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.image(rec.get("poster_path", ""), use_container_width=True)
                    with col2:
                        st.markdown(f"### 🎬 {rec['title']} ({rec.get('year', 'Unknown')})")
                        st.write(f"⭐ {rec.get('rating', 'N/A')}")
            else:
                st.info("No similar movies found.")
        else:
            st.warning("🚫 Movie not found.")

# 🎥 Genre Recommendations
with tab3:
    st.header("🎥 Browse by Genre")
    genre = st.selectbox("Pick a Genre", [
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
                    st.image(movie.get("poster_path", ""), use_container_widthh=True)
                with col2:
                    st.markdown(f"### 🎬 {movie['title']} ({movie.get('year', 'Unknown')})")
                    st.write(f"⭐ {movie.get('rating', 'N/A')}")
                    st.write(movie.get("overview", "No description available."))
        else:
            st.warning("No movies found in this genre.")

# 🎲 Surprise Me!
with tab4:
    st.header("🎲 Surprise Me With a Movie")
    if st.button("Give me a movie!"):
        movie = get_random_movie()
        if movie:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(movie.get("poster_path", ""), use_container_width=True)
            with col2:
                st.markdown(f"### 🎬 {movie['title']} ({movie.get('year', 'Unknown')})")
                st.write(f"⭐ {movie.get('rating', 'N/A')}")
                st.write(movie.get("overview", "No description available."))

                watch = movie.get("watch_providers", {})
                if watch and any(watch.values()):
                    st.markdown("**📍 Where to Watch:**")
                    if watch.get("streaming"):
                        st.write(f"📺 Streaming: {', '.join(watch['streaming'])}")
                    if watch.get("rent"):
                        st.write(f"💰 Rent: {', '.join(watch['rent'])}")
                    if watch.get("buy"):
                        st.write(f"🛒 Buy: {', '.join(watch['buy'])}")
                else:
                    st.write("No watch providers available.")

            cast = movie.get("cast", [])
            if cast:
                st.subheader("🎭 Top Billed Cast")
                cols = st.columns(min(5, len(cast)))
                for i, actor in enumerate(cast[:5]):
                    with cols[i]:
                        st.image(actor.get("profile_pic", ""), width=100)
                        st.write(f"**{actor['name']}**")
                        st.caption(f"as {actor['character']}")
        else:
            st.warning("Couldn't fetch a random movie.")
