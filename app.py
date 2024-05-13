import streamlit as st
import pickle
import pandas as pd

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
import requests


similarity = pickle.load(open('similarity.pkl', 'rb'))

# for the posters of the recommended movies - we will TMDB API for that
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=1552b9b1459200a071cb0d0044119db3&language=en-US'.format(movie_id))

    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    print(response.text)
def recommend(movie):
    # sort but by retaiing the index of the list we can use enumerate function for this as well
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        # fetch poster from API
    return recommended_movies, recommended_movies_posters


st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
"Type in Movie to get similar movie recommendations?",
(movies['title'].values))

#st.button("Recommend", type="primary")
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

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


# earlier I was using st.write(recommend(selected_movie_name)) without using the for loop . It was returning me a entire
# list but using for loop we could iter over the entire list item by item and get a clear print of recommendations
