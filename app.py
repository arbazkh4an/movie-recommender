import streamlit as st
import pickle
import pandas as pd
import os
import gdown

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Download similairty.pkl from Google Drive if not present
def download_file_from_google_drive(file_id, destination):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, destination, quiet=False, fuzzy=True)

# Download the file before loading
SIMILARITY_FILE_ID = '1eAgQhDE6fi4d-pAAHPWWtMQE8abGGVQC'
download_file_from_google_drive(SIMILARITY_FILE_ID, 'similairty.pkl')

if not os.path.exists('similairty.pkl'):
    st.error("similairty.pkl not found! Please check the download link or permissions.")
    st.stop()
else:
    try:
        similarity = pickle.load(open('similairty.pkl', 'rb'))
    except Exception as e:
        st.error(f"Failed to load similairty.pkl: {e}")
        st.stop()

def recommned(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    # Debug info removed
    # if hasattr(similarity, "keys"):
    #     st.write("Similarity keys:", list(similarity.keys())[:10])
    # elif hasattr(similarity, "shape"):
    #     st.write("Similarity shape:", similarity.shape)
    # else:
    #     st.write("Similarity type:", type(similarity))
    # st.write("Movie index for selected movie:", int(movie_index))
    # Defensive check for dicts
    if hasattr(similarity, "keys") and int(movie_index) not in similarity:
        st.error(f"Index {int(movie_index)} not found in similarity keys: {list(similarity.keys())[:10]} ...")
        return []
    distances = similarity[int(movie_index)]
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