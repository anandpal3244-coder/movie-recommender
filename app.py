import streamlit as st
import pandas as pd
import pickle
import requests
import os
import gdown

API_KEY = st.secrets["TMDB_API_KEY"]
# ---------- DOWNLOAD FILE IF NOT EXISTS ----------

SIMILARITY_PATH = "similarity.pkl"

if not os.path.exists(SIMILARITY_PATH):
    url = "https://drive.google.com/uc?id=12-YwOTrYd3IvwPC7A__6TnnYWSPG8DSQ"
    gdown.download(url, SIMILARITY_PATH, quiet=False)

# ---------- LOAD FILES ----------

movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)

similarity = pickle.load(open(SIMILARITY_PATH,'rb'))

st.title("🎬 Movie Recommender System")

# Fetch poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    data = requests.get(url).json()

    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


selected_movie = st.selectbox(
    "Select a Movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0])
        st.caption(names[0])

    with col2:
        st.image(posters[1])
        st.caption(names[1])

    with col3:
        st.image(posters[2])
        st.caption(names[2])

    with col4:
        st.image(posters[3])
        st.caption(names[3])

    with col5:
        st.image(posters[4])
        st.caption(names[4])