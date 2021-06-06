import cv2
import streamlit as st
import base64

def app():
    main_bg = 'sketch_bck.png'

    st.markdown(
        f"""
        <style>
        .reportview-container {{
            background: url(data:image/png;base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("crayon sketch")
    run = st.checkbox('Run')
    st.markdown("""
    ### ☝️ check or uncheck this box to turn the webcam on or off
    An openCV web-app built using streamlit
    """, unsafe_allow_html=True)
    FRAME_WINDOW = st.image([])
    #Our sketch generating function
    def sketch(image):
        # Convert image to grayscale and invert
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        invert = cv2.bitwise_not(img_gray)

        # Clean up image using Guassian Blur, removing noise
        img_gray_blur = cv2.GaussianBlur(invert, (21,21), 0)
        invert_blur = cv2.bitwise_not(img_gray_blur)


        mask = cv2.divide(img_gray, invert_blur, scale=256.0)
        return mask


    # Initialize webcam, cap is the object provided by VideoCapture
    # It contains a boolean indicating if it was sucessful (ret)
    # It also contains the images collected from the webcam (frame)
    cap = cv2.VideoCapture(0)

    while run:
        ret, frame = cap.read()
        frame = cv2.cvtColor(sketch(frame), cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

    if not run:
        st.write('cam off')
        cap.release()
        cv2.destroyAllWindows()