import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("🎬 Movie Recommendation System")

@st.cache_data
def load_data():
    df = pd.read_csv("movies.csv")
    df["genres"] = df["genres"].str.replace("|", " ", regex=False)
    return df

movies = load_data()

tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["genres"])

cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def recommend_movies(title, n=5):
    idx = movies[movies["title"].str.contains(title, case=False)].index
    if len(idx) == 0:
        return []
    idx = idx[0]
    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:n+1]
    return movies["title"].iloc[[i[0] for i in scores]]

movie_choice = st.selectbox("Select a movie:", movies["title"])

if st.button("Recommend"):
    results = recommend_movies(movie_choice)
    st.subheader("Recommended Movies")
    for movie in results:
        st.write("🎥", movie)
