import cv2
import numpy as np
import streamlit as st
import base64

def app():
    main_bg = 'bck.gif'

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

    st.title("Live Ball Tracking")
    run = st.checkbox('Run')
    st.markdown("""
    ### ☝️ check or uncheck this box to turn the webcam on or off
    An openCV web-app built using streamlit
    """, unsafe_allow_html=True)
    FRAME_WINDOW = st.image([])

    cap = cv2.VideoCapture(0)
    # define range of purple color in HSV
    lower_red = np.array([160,100,20])
    upper_red = np.array([179,255,255])

    #lower_red = np.array([125,100,20])
    #upper_red = np.array([255,255,255])

    # Create empty points array
    points = []

    # Get default camera window size
    ret, frame = cap.read()
    Height, Width = frame.shape[:2]
    frame_count = 0

    while run:

        # Capture webcame frame
        ret, frame = cap.read()
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv_img, lower_red, upper_red)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        # Find contours, OpenCV 3.X users use this line instead
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Create empty centre array to store centroid center of mass
        center = int(Height / 2), int(Width / 2)

        if len(contours) > 0:

            # Get the largest contour and its center
            c = max(contours, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            try:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            except:
                center = int(Height / 2), int(Width / 2)

            # Allow only countors that have a larger than 15 pixel radius
            if radius > 25:
                # Draw cirlce and leave the last center creating a trail
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                cv2.circle(frame, center, 5, (0, 255, 0), -1)

        # Log center points
        points.append(center)

        # loop over the set of tracked points
        if radius > 25:
            for i in range(1, len(points)):
                try:
                    cv2.line(frame, points[i - 1], points[i], (0, 255, 0), 2)
                except:
                    pass

            # Make frame count zero
            frame_count = 0
        else:
            # Count frames
            frame_count += 1

            # If we count 10 frames without object lets delete our trail
            if frame_count == 10:
                points = []
                # when frame_count reaches 20 let's clear our trail
                frame_count = 0

        # Display our object tracker
        frame = cv2.flip(frame, 1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

    if not run:
        st.write('cam off')
        cap.release()
        cv2.destroyAllWindows()
