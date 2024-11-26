from Threading import *

def preprocessFrame(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv[..., 2] = cv2.normalize(hsv[..., 2], None, alpha=50, beta=255, norm_type=cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    hsv[..., 2] = clahe.apply(hsv[..., 2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def detectLandmarks(frame):
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = faceMesh.process(rgbFrame)
    return output.multi_face_landmarks if output.multi_face_landmarks else None


def drawLandmarks(frame, landmarks):
    for id, landmark in enumerate(landmarks):
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
    for landmark in [landmarks[145], landmarks[159], landmarks[474], landmarks[475]]:
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)

def moveMouseWithEye(landmarks):
    rightEye = [landmarks[474], landmarks[475], landmarks[476], landmarks[477]]
    eyeLeftCorner = landmarks[33]
    eyeRightCorner = landmarks[133]
    eyeWidth = eyeRightCorner.x - eyeLeftCorner.x
    irisCenterX = sum([p.x for p in rightEye]) / len(rightEye)
    relativeX = (irisCenterX - eyeLeftCorner.x) / eyeWidth
    screenX = screenWidth * (1 - relativeX)
    irisCenterY = sum([p.y for p in rightEye]) / len(rightEye)
    screenY = screenHeight * irisCenterY
    pyautogui.moveTo(screenX, screenY)
    current_cursor_position = pyautogui.position()
    print(f"Cursor moved to: {current_cursor_position}")





def moveMouseWithNose(landmarks):
    noseTip = landmarks[1]
    noseX = noseTip.x 
    noseY = noseTip.y  
    screenX = screenWidth * noseX
    screenY = screenHeight * noseY
    print(f"Nose X: {noseX}, Nose Y: {noseY}")
    print(f"Screen X: {screenX}, Screen Y: {screenY}")
    pyautogui.moveTo(screenX, screenY)
    current_cursor_position = pyautogui.position()
    print(f"Cursor moved to: {current_cursor_position}")




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
                moveMouseWithEye(landmarks[0].landmark)
                drawLandmarks(frame, landmarks[0].landmark)
            cv2.imshow('Eye Controlled Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    cam.release()
    cv2.destroyAllWindows()

def noseControlledMouse():
    while True:
        try:
            ret, frame = cam.read()
            if not ret:
                continue
            frame = cv2.flip(frame, 1)
            frame = preprocessFrame(frame)
            landmarks = detectLandmarks(frame)
            if landmarks:
                moveMouseWithNose(landmarks[0].landmark)
                drawLandmarks(frame, landmarks[0].landmark)
            cv2.imshow('Nose Controlled Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except Exception as e:
            print(f"Error: {e}")
            break

    cam.release()
    cv2.destroyAllWindows()
