from Threading import *


def detectLandmarks(frame):
    rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = faceMesh.process(rgbFrame)
    return output.multi_face_landmarks if output.multi_face_landmarks else None

def moveMouse(landmarks, frameWidth, frameHeight):
    for id, landmark in enumerate(landmarks[474:478]):
        if id == 1:
            screenX = screenWidth * landmark.x
            screenY = screenHeight * landmark.y
            pyautogui.moveTo(screenX, screenY)

def detectBlinks(landmarks):
    leftEye = [landmarks[145], landmarks[159]]
    rightEye = [landmarks[374], landmarks[386]]
    leftBlink = (leftEye[0].y - leftEye[1].y) < 0.004
    rightBlink = (rightEye[0].y - rightEye[1].y) < 0.004
    # Left Click
    if leftBlink:
        pyautogui.click(button='left')
        time.sleep(1)
    # Right Click
    if rightBlink:
        pyautogui.click(button='right')
        time.sleep(1)

def drawLandmarks(frame, landmarks):
    for id, landmark in enumerate(landmarks[474:478]):
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
    global isRunning
    
    while isRunning:
        ret, frame = cam.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        landmarks = detectLandmarks(frame)

        if landmarks:
            moveMouse(landmarks[0].landmark, frame.shape[1], frame.shape[0])
            detectBlinks(landmarks[0].landmark)
            drawLandmarks(frame, landmarks[0].landmark)

        cv2.imshow('Eye Controlled Mouse', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            isRunning = False
    
    cam.release()
    cv2.destroyAllWindows()



def startEyeControlledMouse():
    return runInThread(eyeControlledMouse)

def stopEyeControlledMouse(thread):
    global isRunning
    isRunning = False
    thread.join()