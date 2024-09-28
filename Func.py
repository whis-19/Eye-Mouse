from Threading import *


# Preprocess frame
def preprocessFrame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv[..., 2] = cv2.normalize(hsv[..., 2], None, alpha=50, beta=255, norm_type=cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    hsv[..., 2] = clahe.apply(hsv[..., 2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# Detect landmarks
def detectLandmarks(frame):
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = faceMesh.process(rgbFrame)
    return output.multi_face_landmarks if output.multi_face_landmarks else None




def moveMouseWithEye(landmarks):
    # Use landmarks for right eye (using points from Mediapipe FaceMesh)
    rightEye = [landmarks[474], landmarks[475], landmarks[476], landmarks[477]]  # Iris landmarks
    eyeLeftCorner = landmarks[33]  # Outer corner of the right eye
    eyeRightCorner = landmarks[133]  # Inner corner of the right eye

    # Calculate the relative movement of the iris within the eye
    eyeWidth = eyeRightCorner.x - eyeLeftCorner.x
    irisCenterX = sum([p.x for p in rightEye]) / len(rightEye)
    
    # Map eye movement to screen coordinates
    relativeX = (irisCenterX - eyeLeftCorner.x) / eyeWidth  # Horizontal ratio
    screenX = screenWidth * (1 - relativeX)  # Move the cursor inversely for natural movement
    
    # Move the cursor on the Y axis if needed (can be refined with eye height)
    irisCenterY = sum([p.y for p in rightEye]) / len(rightEye)
    screenY = screenHeight * irisCenterY
    
    # Move the actual cursor
    pyautogui.moveTo(screenX, screenY)
    
    # Print current cursor position
    current_cursor_position = pyautogui.position()  # Get the current cursor position
    print(f"Cursor moved to: {current_cursor_position}")  # Print the cursor position

# Draw landmarks on the frame for visualization
def drawLandmarks(frame, landmarks):
    for id, landmark in enumerate(landmarks):
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

    for landmark in [landmarks[145], landmarks[159], landmarks[474], landmarks[475]]:
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

# Eye controlled mouse function
def eyeControlledMouse():
    while True:
        try:
            ret, frame = cam.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)  # Flip horizontally for a mirrored view
            frame = preprocessFrame(frame)  # Optional preprocessing

            landmarks = detectLandmarks(frame)  # Detect facial landmarks

            if landmarks:
                # Move mouse based on eye landmarks (iris/retina)
                moveMouseWithEye(landmarks[0].landmark)
                # Draw landmarks for visualization
                drawLandmarks(frame, landmarks[0].landmark)

            # Show webcam feed with landmarks
            cv2.imshow('Eye Controlled Mouse', frame)

            # Quit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    cam.release()
    cv2.destroyAllWindows()


