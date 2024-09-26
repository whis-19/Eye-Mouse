from Threading import *



def preprocessFrame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv[..., 2] = cv2.normalize(hsv[..., 2], None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    
    hsv[..., 2] = cv2.normalize(hsv[..., 2], None, alpha=50, beta=255, norm_type=cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    hsv[..., 2] = clahe.apply(hsv[..., 2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def detectLandmarks(frame):
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = faceMesh.process(rgbFrame)
    return output.multi_face_landmarks if output.multi_face_landmarks else None

def moveMouse(landmarks):
    if landmarks:
        screenX = screenWidth * landmarks[1].x
        screenY = screenHeight * landmarks[1].y
        current_x, current_y = pyautogui.position()
        smooth_x = current_x + (screenX - current_x) * 0.1
        smooth_y = current_y + (screenY - current_y) * 0.1
        pyautogui.moveTo(smooth_x, smooth_y)

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

def drawLandmarks(frame, landmarks):
    for id, landmark in enumerate(landmarks):
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    for landmark in [landmarks[145], landmarks[159]]:
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

    for landmark in [landmarks[374], landmarks[386]]:
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)


def eyeControlledMouse():
    while True:
        try:
            ret, frame = cam.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            frame = preprocessFrame(frame)  

            landmarks = detectLandmarks(frame)

            if landmarks:
                moveMouse(landmarks[0].landmark)
                detectBlinks(landmarks[0].landmark)
                drawLandmarks(frame, landmarks[0].landmark)

            cv2.imshow('Eye Controlled Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    cam.release()