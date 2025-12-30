import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===============================
# App Title
# ===============================
st.title("🎬 Movie Recommendation System")
st.write("Recommend movies based on genre similarity")

# ===============================
# Load Data
# ===============================
@st.cache_data
def load_data():
    movies = pd.read_csv("movies.csv")
    movies["genres"] = movies["genres"].str.replace("|", " ", regex=False)
    return movies

movies = load_data()

# ===============================
# Vectorization
# ===============================
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["genres"])


cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# ===============================
# Recommendation Function
# ===============================
def recommend_movies(title, num_recommendations=5):
    idx = movies[movies["title"].str.contains(title, case=False)].index
    
    if len(idx) == 0:
        return []
    
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:num_recommendations + 1]
    
    movie_indices = [i[0] for i in sim_scores]
    return movies["title"].iloc[movie_indices]

# ===============================
# Streamlit UI
# ===============================
movie_list = movies["title"].values
selected_movie = st.selectbox("Choose a movie:", movie_list)

if st.button("Recommend"):
    recommendations = recommend_movies(selected_movie)
    
    if len(recommendations) == 0:
        st.warning("Movie not found.")
    else:
        st.subheader("Recommended Movies:")
        for movie in recommendations:
            st.write("🎥", movie)
