import cv2
import mediapipe as mp
import pyautogui
import threading
import time
import keyboard

# import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"



# Control loop variable

# Initialize video capture and face mesh
cam = cv2.VideoCapture(0)
faceMesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screenWidth, screenHeight = pyautogui.size()
print("Screen Width:", screenWidth, "Screen Height:", screenHeight)  # Debugging screen size
