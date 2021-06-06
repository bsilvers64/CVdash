import streamlit as st
import cv2
import numpy as np
import base64
from canny_edge import canny_detector
from PIL import Image, ImageEnhance

def app():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')


    def detect_faces(image):
        new_img = np.array(image.convert('RGB'))
        img = cv2.cvtColor(new_img, 1)
        gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        # Draw rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        return img, faces


    def detect_eyes(image):
        new_img = np.array(image.convert('RGB'))
        img = cv2.cvtColor(new_img, 1)
        gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        return img


    def detect_smiles(image):
        new_img = np.array(image.convert('RGB'))
        img = cv2.cvtColor(new_img, 1)
        gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        # Detect Smiles
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
        return img


    def cartoonize_image(image):
        new_img = np.array(image.convert('RGB'))
        img = cv2.cvtColor(new_img, 1)
        gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
        # Edges
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        # Color
        color = cv2.bilateralFilter(img, 9, 300, 300)
        # Cartoon
        cartoon = cv2.bitwise_and(color, color, mask=edges)

        return cartoon


    def color_quantization(img):
    # Transform the image
       data = np.float32(img).reshape((-1, 3))
    # Determine criteria
       criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    # Implementing K-Means
       ret, label, center = cv2.kmeans(data, 9, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
       center = np.uint8(center)
       result = center[label.flatten()]
       result = result.reshape(img.shape)
       return result



    """Face Detection App"""
    our_image = Image.open('sample.jpg')

    main_bg = 'bck4.gif'

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


    st.title("Face Detection App")
    st.text("Build with Streamlit and OpenCV")

    activities = ["Detection", "About"]
    choice = st.sidebar.selectbox("Select Activty", activities)

    if choice == 'Detection':
            st.subheader("Face Detection")

            image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

            if image_file is not None:
                our_image = Image.open(image_file)
                st.text("Original Image")
                st.image(our_image)

            enhance_type = st.sidebar.radio("Enhance Type",
                                            ["Original", "Gray-Scale", "Contrast", "Brightness", "Blurring",
                                             "Color-Quantization"])
            if enhance_type == 'Gray-Scale':
                new_img = np.array(our_image.convert('RGB'))
                img = cv2.cvtColor(new_img, 1)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                st.image(gray)

            elif enhance_type == 'Contrast':
                c_rate = st.sidebar.slider("Contrast", 0.5, 3.5)
                enhancer = ImageEnhance.Contrast(our_image)
                img_output = enhancer.enhance(c_rate)
                st.image(img_output)

            elif enhance_type == 'Brightness':
                c_rate = st.sidebar.slider("Brightness", 0.5, 3.5)
                enhancer = ImageEnhance.Brightness(our_image)
                img_output = enhancer.enhance(c_rate)
                st.image(img_output)

            elif enhance_type == 'Blurring':
                new_img = np.array(our_image.convert('RGB'))
                blur_rate = st.sidebar.slider("Brightness", 0.5, 3.5)
                img = cv2.cvtColor(new_img, 1)
                blur_img = cv2.GaussianBlur(img, (11, 11), blur_rate)
                st.image(blur_img)

            elif enhance_type == 'Color-Quantization':
                pil_image = our_image.convert('RGB')
                open_cv_image = np.array(pil_image)
                # Convert RGB to BGR
                st.image(color_quantization(open_cv_image))

            elif enhance_type == 'Original':
                st.image(our_image, width=300)
            else:
                st.image(our_image, width=300)

            # Face Detection
            task = ["Faces", "Smiles", "Eyes", "Canny edge detection", "Cartoonify"]
            feature_choice = st.sidebar.selectbox("Find Features", task)
            if st.button("Process"):

                if feature_choice == 'Faces':
                    result_img, result_faces = detect_faces(our_image)
                    st.image(result_img)

                    st.success("Found {} faces".format(len(result_faces)))
                elif feature_choice == 'Smiles':
                    result_img = detect_smiles(our_image)
                    st.image(result_img)


                elif feature_choice == 'Eyes':
                    result_img = detect_eyes(our_image)
                    st.image(result_img)

                elif feature_choice == 'Cartoonify':
                    result_img = cartoonize_image(our_image)
                    st.image(result_img)

                elif feature_choice == 'Canny edge detection':
                    pil_image = our_image.convert('RGB')
                    cv_image = np.array(pil_image)
                    result_canny = canny_detector(cv_image)
                    st.image(result_canny, clamp=True)



