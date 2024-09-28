from Threading import *



# Frame Preprocessing
def preprocessFrame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv[..., 2] = cv2.normalize(hsv[..., 2], None, alpha=50, beta=255, norm_type=cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    hsv[..., 2] = clahe.apply(hsv[..., 2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# Detect Landmarks
def detectLandmarks(frame):
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = faceMesh.process(rgbFrame)
    return output.multi_face_landmarks if output.multi_face_landmarks else None

# Head Movement Detection for Mouse Control and Visual Cursor
def moveMouseWithHead(landmarks, frame):
    if landmarks:
        nose_landmark = landmarks[1]  # Nose landmark (typically used for head tracking)
        screenX = screenWidth * nose_landmark.x
        screenY = screenHeight * nose_landmark.y
        current_x, current_y = pyautogui.position()
        
        # Smoothing for smoother cursor movement
        smooth_x = current_x + (screenX - current_x) * 0.1
        smooth_y = current_y + (screenY - current_y) * 0.1

        # Move the real system mouse
        pyautogui.moveTo(smooth_x, smooth_y)

        # Draw a circle on the frame to represent the visual cursor
        cv2.circle(frame, (int(smooth_x), int(smooth_y)), 10, (255, 0, 0), -1)  # Blue circle as cursor

# Detect Blinks (Optional, but you can keep it)
def detectBlinks(landmarks):
    leftEye = [landmarks[145], landmarks[159]]
    rightEye = [landmarks[374], landmarks[386]]
    leftBlink = (leftEye[0].y - leftEye[1].y) < 0.005 
    rightBlink = (rightEye[0].y - rightEye[1].y) < 0.005 
    
    # Left Click
    if leftBlink:
        pyautogui.click(button='left')
        time.sleep(1)
    # Right Click
    if rightBlink:
        pyautogui.click(button='right')
        time.sleep(1)

# Drawing landmarks for visualization
def drawLandmarks(frame, landmarks):
    for id, landmark in enumerate(landmarks):
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    for landmark in [landmarks[145], landmarks[159]]:  # Left eye
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

    for landmark in [landmarks[374], landmarks[386]]:  # Right eye
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

# Eye/Head Controlled Mouse in a Thread
def eyeControlledMouse():
    while True:
        try:
            ret, frame = cam.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)  # Flip horizontally for natural interaction
            frame = preprocessFrame(frame)  # Optional preprocessing

            landmarks = detectLandmarks(frame)  # Detect facial landmarks

            if landmarks:
                moveMouseWithHead(landmarks[0].landmark, frame)  # Move mouse and show visual cursor
                detectBlinks(landmarks[0].landmark)  # Optional blink detection
                drawLandmarks(frame, landmarks[0].landmark)  # Draw landmarks for debugging

            # Display the frame
            cv2.imshow('Head Controlled Mouse with Visual Cursor', frame)

            # Quit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    cam.release()
    cv2.destroyAllWindows()