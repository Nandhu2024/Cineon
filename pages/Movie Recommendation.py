import streamlit as st
import requests
from imdb import Cinemagoer

# Create an instance of the IMDb class
ia = Cinemagoer()

# Function to fetch the poster URL from TMDb
def fetch_poster(imdb_id):
    search_url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&external_source=imdb_id"
    response = requests.get(search_url)
    data = response.json()
    
    # Debugging: Print the response from TMDb API
    st.write("TMDb API response:", data)
    
    if data.get('movie_results'):
        poster_path = data['movie_results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
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
            poster_url = fetch_poster(imdb_id)

            # Display movie data
            st.subheader(f"Title: {movie_data.get('title')}")
            st.text(f"Year: {movie_data.get('year')}")
            st.text(f"Genre: {', '.join(movie_data.get('genre', []))}")
            st.text(f"Director: {', '.join(movie_data.get('director', []))}")
            st.text(f"Actors: {', '.join(movie_data.get('actors', []))}")
            st.text(f"Plot: {movie_data.get('plot')}")
            st.text(f"Rating: {movie_data.get('rating')}")

            if poster_url:
                st.image(poster_url, caption='Movie Poster')
            else:
                st.text("Poster not available.")
