import mediapipe as mp
import cv2
import streamlit as st
import base64

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


def app():
    main_bg = 'bck8.gif'

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

    st.title("Human pose esimation with facial landmarks")
    run = st.checkbox('Run')
    st.markdown("""
    ### ☝️ check or uncheck this box to turn the webcam on or off
    An openCV web-app built using streamlit
    """, unsafe_allow_html=True)
    FRAME_WINDOW = st.image([])

    cap = cv2.VideoCapture(0)
    # Initiate holistic model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while run:
            ret, frame = cap.read()

            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Make Detections
            results = holistic.process(image)
            # print(results.face_landmarks)

            # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks

            # Recolor image back to BGR for rendering
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 1. Draw face landmarks
            mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
                                      mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
                                      )

            # 2. Right hand
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                                      )

            # 3. Left Hand
            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                                      )

            # 4. Pose Detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                                      mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                      )

            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)

        if not run:
            st.write('cam off')
            cap.release()
            cv2.destroyAllWindows()

