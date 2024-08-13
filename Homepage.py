import pickle
import streamlit as st
import requests
from st_paywall import add_auth


st.set_page_config(
    page_title="CineOn",
    page_icon="🎥"
)

st.title('Welcome to CiNeon/this is working')
add_auth(st)
st.write(st.session_state.email)
st.text('Latest News')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.markdown('')
st.text('Coming Soon')
st.sidebar.success('Built with Streamlit')
