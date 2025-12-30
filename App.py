import streamlit as st
import pandas as pd

# ===============================
# Page Config (Cleaner Look)
# ===============================
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ===============================
# Title Section
# ===============================
st.title("🎬 Movie Recommender")
st.caption("Discover movies based on genres and popularity")

# ===============================
# Load Data
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    return df

movies = load_data()

# ===============================
# Extract Genres
# ===============================
all_genres = sorted(
    {genre for genres in movies["genres"] for genre in genres.split("|")}
)

# ===============================
# Sidebar Controls
# ===============================
st.sidebar.header("🎯 Filter Movies")

selected_genres = st.sidebar.multiselect(
    "Select genre(s)",
    all_genres
)

num_movies = st.sidebar.slider(
    "Number of recommendations",
    min_value=5,
    max_value=30,
    value=10
)

sort_option = st.sidebar.selectbox(
    "Sort results by",
    ["Popularity (if available)", "Alphabetical"]
)

# ===============================
# Recommendation Logic
# ===============================
def genre_match(genres):
    return any(g in genres for g in selected_genres)

if st.sidebar.button("🎥 Recommend Movies"):
    if not selected_genres:
        st.warning("Please select at least one genre.")
    else:
        results = movies[movies["genres"].apply(genre_match)]

        # Sorting logic
        if sort_option == "Popularity (if available)" and "popularity" in results.columns:
            results = results.sort_values("popularity", ascending=False)
        else:
            results = results.sort_values("title")

        st.subheader("🍿 Recommended Movies")

        if results.empty:
            st.info("No movies found for the selected genre(s).")
        else:
            # Display movies in a clean card-style layout
            for _, row in results.head(num_movies).iterrows():
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### 🎞 {row['title']}")
                        st.markdown(f"**Genres:** {row['genres']}")
                    with col2:
                        if "popularity" in row:
                            st.metric("Popularity", row.get("popularity", "N/A"))
                    st.divider()
