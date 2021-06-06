import cv2
import mediapipe as mp
import time
import streamlit as st
import base64

def app():
    main_bg = 'bck3.png'

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


    st.title("Live face Recognition")
    run = st.checkbox('Run')
    st.markdown("""
    ### ☝️ check or uncheck this box to turn the webcam on or off
    An openCV web-app built using streamlit
    """, unsafe_allow_html=True)
    mpFaceDetection = mp.solutions.face_detection
    mpDraw = mp.solutions.drawing_utils
    faceDetection = mpFaceDetection.FaceDetection(0.75)

    def face_rec(img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = faceDetection.process(imgRGB)
        if results.detections:
            for id, detection in enumerate(results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(img, bbox, (255, 130, 0), 2)
                cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                            (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_PLAIN,
                            2, (93, 11, 227), 2)

        return img


    FRAME_WINDOW = st.image([])
    cap = cv2.VideoCapture(0)
    pTime = 0

    while run:
        ret, frame = cap.read()
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(frame, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (0, 255, 0), 2)
        #cv2.imshow('Our Live Sketcher', face_rec(frame))
        frame = face_rec(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        FRAME_WINDOW.image(frame)
        #if cv2.waitKey(10) == 13: #13 is the Enter Key
        #    break

    if not run:
        cap.release()
        st.write('cam off')
        cv2.destroyAllWindows()

