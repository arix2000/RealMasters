import streamlit as st
from frontend.home_page import render_page

st.set_page_config(layout="wide", page_title="Real Master", initial_sidebar_state="expanded")

render_page()
