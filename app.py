import streamlit as st
import pickle
import pandas as pd

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similairty.pkl', 'rb'))

def recommned(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies= []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies


st.title("Movie Recommendation")

movie_name = st.selectbox(
    "Choose movie for recommendation",
    movies['title'].values
)



if st.button("Predict"):
    recomendations = recommned(movie_name)
    for i in recomendations:
     st.write(i)