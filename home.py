import streamlit as st
import base64


def app():
    main_bg = 'bck2.gif'

    st.markdown(
        f"""
        <style>
        .reportview-container {{
            background: url(data:image/gif;base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    st.title('Home')

    st.write('This is the `home page`')

    st.write('In this app, we will be showcasing a multiple openCV tools and implementations')
