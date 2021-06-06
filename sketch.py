import streamlit as st
import live_sketch_2
import live_sketch

def app():
    PAGES = {
        "line sketch": live_sketch,
        "crayon sketch": live_sketch_2
    }
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()
