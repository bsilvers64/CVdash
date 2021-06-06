import cv2
import pytesseract
import numpy as np
import base64
from PIL import Image
import streamlit as st

pytesseract.pytesseract.tesseract_cmd = r'D:\other\Tesseract_OCR\tesseract'

def app():

    main_bg = 'ocr_bck.gif'

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
    st.title("optical character recognition")

    our_image = Image.open('text.png')

    image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

    if image_file is not None:
        our_image = Image.open(image_file)
        st.text("Original Image with ocr output and extracted text")

    our_image = our_image.convert('RGB')
    pil_image = our_image
    img = np.array(pil_image)
    st.image(our_image, clamp=True)
    text_string = pytesseract.image_to_string(img)
    #st.markdown(f"""<p style="background-color:#192f3e;">{text_string}</p>""", unsafe_allow_html=True)
    st.markdown(text_string)

    conf = r'--oem 1'
    boxes = pytesseract.image_to_data(img, config=conf)


    for i, b in enumerate(boxes.splitlines()):
        if i:
            b = b.split()
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(img, (x, y), (w + x, h + y), (150, 120, 16), 2)
                cv2.putText(img, b[11], (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.65, (30,98,218), 2)

    st.image(img, clamp=True)
