import pickle
import streamlit as st
import requests

movies = pickle.load(open('movie_list.pkl','rb'))
similarity_angle = pickle.load(open('similarity_angle.pkl','rb'))
movie_list = movies['title'].values

def link_movie(movie_id):
    """generate movie link based on id"""
    path_link = "https://www.themoviedb.org/movie/{}".format(movie_id)
    return path_link

def fetch_poster_user_rating(movie_id):
    """generate poster link based on id"""
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=ca218247dd7a4747395e5393caf26643&language=en-US'.format(movie_id))
    data = response.json()
    rating = round(data['vote_average'],1)
    path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + path
    return full_path, rating

def recommend(selected_movie):
    movie_index = movies.index[movies['title'] == selected_movie].tolist()[0]  # we need values only not list so we used [0] to get first value of list
    similarity = similarity_angle[movie_index]  # angles without index
    angle_with_index = enumerate(similarity)  # angles with index
    angle_tuple = list(angle_with_index)  # list of tuple of angles
    descending_angle = sorted(angle_tuple, key=lambda tup: tup[1],reverse=True)  # sorted in descending order w.r.t angle
    movie_recommend = descending_angle[1:number+1]  # selecting angle from 2nd row until 7th row
    recommended_movies = []
    movie_posters = []
    movie_link = []
    user_rating = []
    for i in movie_recommend:
        movie_id = movies.iloc[i[0], 0]
        recommended_movies.append(movies.iloc[i[0], 1])  # i[0] gives us first elements of all tuples.
        movie_posters.append(fetch_poster_user_rating(movie_id)[0])
        movie_link.append(link_movie(movie_id))
        user_rating.append(fetch_poster_user_rating(movie_id)[1])
    return recommended_movies,movie_posters,movie_link,user_rating



st.set_page_config(layout="wide")

st.title("Movie Recommendation System")

selected_movie = st.selectbox("Type or select a movie from the dropdown",movie_list)

number = st.slider('Please select number of recommended movies', 1, 10, 5)

if st.button('Recommend'):
    recommended_movies,movie_posters,movie_link,user_rating = recommend(selected_movie)

    movie_cols = st.columns(number)

    for cols, title, posters, link, rate in zip(movie_cols, recommended_movies,movie_posters, movie_link, user_rating):
        with cols:
            st.write('User Rating: ',rate)
            st.image(posters)
            st.markdown(f"<a style='display: block; text-align: center;' href='{link}'>{title}</a>",unsafe_allow_html=True)


footer = """
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
    <footer>
        <div style='visibility: visible;margin-top:7rem;justify-content:center;display:flex;'>
            <p style="font-size:1.1rem;">
                Made by Md Golam Rassel Lincoln and follow me here
                &nbsp;
                <a href="https://www.linkedin.com/in/md-golam-rassel-lincoln-8474b2116">
                    <svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" fill="white" class="bi bi-linkedin" viewBox="0 0 16 16">
                        <path d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854V1.146zm4.943 12.248V6.169H2.542v7.225h2.401zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248-.015-.709-.52-1.248-1.342-1.248-.822 0-1.359.54-1.359 1.248 0 .694.521 1.248 1.327 1.248h.016zm4.908 8.212V9.359c0-.216.016-.432.08-.586.173-.431.568-.878 1.232-.878.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252-1.274 0-1.845.7-2.165 1.193v.025h-.016a5.54 5.54 0 0 1 .016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225h2.4z"/>
                    </svg>          
                </a>
                &nbsp;
                <a href="https://github.com/rassel25">
                    <svg xmlns="http://www.w3.org/2000/svg" width="23" height="23" fill="white" class="bi bi-github" viewBox="0 0 16 16">
                        <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                    </svg>
                </a>
            </p>
        </div>
    </footer>
"""
st.markdown(footer, unsafe_allow_html=True)