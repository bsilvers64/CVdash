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

    st.title("line sketch")
    run = st.checkbox('Run')
    st.markdown("""
    ### ☝️ check or uncheck this box to turn the webcam on or off
    An openCV web-app built using streamlit
    """, unsafe_allow_html=True)
    FRAME_WINDOW = st.image([])

    #Our sketch generating function
    def sketch(image):
        # Convert image to grayscale
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Clean up image using Guassian Blur, removing noise
        img_gray_blur = cv2.GaussianBlur(img_gray, (5,5), 0)

        # Extract edges, suing canny for edge detection
        canny_edges = cv2.Canny(img_gray_blur, 20, 50)

        # Do an invert binarize the image
        re, mask = cv2.threshold(canny_edges, 70, 255, cv2.THRESH_BINARY_INV)
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