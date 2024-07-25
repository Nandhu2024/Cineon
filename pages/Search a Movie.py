
import streamlit as st

import sys
print(sys.executable)

from cinemagoer import Cinemagoer


# Create an instance of the IMDb class
ia = Cinemagoer()

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
            movie_data = {
                'title': movie.get('title'),
                'year': movie.get('year'),
                'genre': movie.get('genres'),
                'director': [director['name'] for director in movie.get('directors')],
                'actors': [actor['name'] for actor in movie.get('cast')],
                'plot': movie.get('plot outline'),
                'rating': movie.get('rating')
            }

            # Display movie data
            st.subheader(f"Title: {movie_data.get('title')}")
            st.text(f"Year: {movie_data.get('year')}")
            st.text(f"Genre: {', '.join(movie_data.get('genre', []))}")
            st.text(f"Director: {', '.join(movie_data.get('director', []))}")
            st.text(f"Actors: {', '.join(movie_data.get('actors', []))}")
            st.text(f"Plot: {movie_data.get('plot')}")
            st.text(f"Rating: {movie_data.get('rating')}")