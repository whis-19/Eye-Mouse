import cv2
import mediapipe as mp
import pyautogui
import threading
import time

# Control loop variable
isRunning = threading.Event()
isRunning.set()

# Initialize video capture and face mesh
cam = cv2.VideoCapture(0)
faceMesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screenWidth, screenHeight = pyautogui.size()
