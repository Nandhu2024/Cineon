import streamlit as st
import requests
from imdb import Cinemagoer

# Create an instance of the IMDb class
ia = Cinemagoer()

# Function to fetch the poster URL from TMDb
def fetch_poster(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key=8265bd1679663a7ea12ac168da84d2e8&query={movie_title}"
    response = requests.get(search_url)
    data = response.json()
    
    
    
    if data.get('results'):
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None
def fetch_person(person_title):
    search_url = f"https://api.themoviedb.org/3/search/person?api_key=8265bd1679663a7ea12ac168da84d2e8&query={person_title}"
    response = requests.get(search_url)
    data = response.json()
    
    
    
    if data.get('results'):
        poster_path = data['results'][0].get('profile_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None
def fetch_movie_id(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key=8265bd1679663a7ea12ac168da84d2e8&query={movie_title}"
    response = requests.get(search_url)
    data = response.json()
    
    if data.get('results'):
        return data['results'][0].get('id')
    return None
def fetch_trailer(movie_id):
    video_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(video_url)
    data = response.json()
    
    if data.get('results'):
        for video in data['results']:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                return f"https://www.youtube.com/embed/{video['key']}"
    return None

st.title("IMDb Movie Data Fetcher")

movie_title = st.text_input("Enter a movie title:")

if st.button("Fetch Movie Data"):
    if not movie_title:
        st.error("Please enter a movie title.")
    else:
        # Search for the movie
        movies = ia.search_movie(movie_title)
        if not movies:
            st.error("Movie not found.")
        else:
            # Get the first movie in the search results
            movie = ia.get_movie(movies[0].movieID)
            imdb_id = movie.movieID  # IMDb ID for TMDb query
            movie_data = {
                'title': movie.get('title'),
                'year': movie.get('year'),
                'genre': movie.get('genres'),
                'director': [director['name'] for director in movie.get('directors')],
                'actors': [actor['name'] for actor in movie.get('cast')],
                'plot': movie.get('plot outline'),
                'rating': movie.get('rating')
            }

            # Fetch the poster URL
            poster_url = fetch_poster(movie_title)
            movie_id = fetch_movie_id(movie_title)

            trailer_url = fetch_trailer(movie_id)

            # Display movie data
            st.subheader(f"Title: {movie_data.get('title')}")
            col1, col2 = st.columns([2, 2])  # Adjust the width ratio as needed

            with col1:
                if poster_url:
                    st.markdown("Movie Poster")
                    st.image(poster_url, caption='Movie Poster', width=200)
                else:
                    st.text("Poster not available.")
                
            with col2:
                if trailer_url:
                    st.markdown("Trailer:")
                    #st.video(trailer_url)
                    st.markdown(f'<iframe width="500" height="300" src="{trailer_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>', unsafe_allow_html=True)
                else:
                    st.text("Trailer not available.")
            
            st.text(f"Year: {movie_data.get('year')}")
            st.text(f"Genre: {', '.join(movie_data.get('genre', []))}")
            st.text(f"Director: {', '.join(movie_data.get('director', []))}")
            #st.text(f"Actors: {', '.join(movie_data.get('actors', []))}")
            actors = movie_data.get('actors', [])
            first_five_actors = actors[:5]
            num_actors = len(first_five_actors)
            columns = st.columns(num_actors)

            for i, actor in enumerate(first_five_actors):
                person_url = fetch_person(actor)
                with columns[i]:
                    if person_url:
                        st.image(person_url, caption=actor, width=100)
                    else:
                        st.text(f"{actor}: Photo not available.")


            st.markdown(f"Actors: {', '.join(first_five_actors)}")
            st.markdown(f"Plot: {movie_data.get('plot')}")
            st.text(f"Rating: {movie_data.get('rating')}")
            
            
