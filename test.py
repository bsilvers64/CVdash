import cv2
import streamlit as st

st.title("Webcam Live Feed")
run = st.checkbox('Run')
st.markdown("""
### ☝️ check or uncheck this box to turn the webcam on or off
An openCV web-app built using streamlit
""", unsafe_allow_html=True)
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(0)

while run:
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)
else:
    st.write('Stopped')

if not run:
    cap.release()