#to deploy write on terminal python -m streamlit run deploy.py
import streamlit as st 
import pickle
import pandas as pd
import requests 

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a62c1e5bc6443590cd4ff8653e3a8b7b'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])[1:6]
    
    recommended = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        #poster
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended.append(movies.iloc[i[0]].title)    
    return recommended, recommended_movies_poster

similarity = pickle.load(open('similarity.pkl','rb'))

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

option = st.selectbox(
    'Enter the movie',
    movies['title'].values
)
if st.button('Recommend'):
    names,posters = recommend(option)
    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
    