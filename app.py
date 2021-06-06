import streamlit as st
from multiapp import MultiApp
import image_manipulation, home, live_face_recog, ball_tracking, faceL_and_body, sketch
import mask_detection, ocr_1, social_distance_detector

app = MultiApp()

st.markdown("""
# <span style="color:#e30b5d;font-size:50px;">CV</span><span style="font-size:45px;">Dash</span>
An openCV web-app built using streamlit
""", unsafe_allow_html=True)

app.add_app("Home", home.app)
app.add_app("Manipulate image and find features", image_manipulation.app)
app.add_app("Live face recognition", live_face_recog.app)
app.add_app("Facial landmarks and human pose detection", faceL_and_body.app)
app.add_app("Real time ball tracking", ball_tracking.app)
app.add_app("Social Distancing Detector", social_distance_detector.app)
app.add_app("Real time Mask Detection", mask_detection.app)
app.add_app("Live sketch", sketch.app)
app.add_app("Optical Character recognition", ocr_1.app)


# The main app
app.run()