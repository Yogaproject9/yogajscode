# Importing all required libraries
import mediapipe as mp
import pickle
import pandas as pd
import cv2
import os
import numpy as np
import math
import time
import multiprocessing
from time import sleep
from playsound import playsound

wait = 15
# wait = 5
wait2 = 10
t_wait = time.time()
t_wait2 = time.time()
# fial treepose flag
fi_fl = 0
c_knee = 0
c_shoulder = 0
c_elbow = 0
posture_output = 0 


# Mediapipe Drawing helpers
mp_drawing = mp.solutions.drawing_utils 
mp_holistic = mp.solutions.holistic 
mp_pose = mp.solutions.pose

# Reading data from .pkl file
with open('yoga/yoga_posture_changed.pkl', 'rb') as f:
    model = pickle.load(f)

# Giving value to the posture
if posture_output <=3:
    posture="vrukshasana_treepose"
elif posture_output <=6:
    posture="tricoaasana"
# Function for calculating the angle
def calc_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = round(np.abs(radians*180.0/np.pi),2)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle


# Function for calculating the distance
def calculateDistance(x1,y1,x2,y2):
    dist1 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    dist = (dist1*100)
    return dist

# cap = cv2.VideoCapture(0)
class VideoCamera(object):

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_holistic = mp.solutions.holistic
        self.video = cv2.VideoCapture('yoga/trim1_2.0x.mp4')
        #self.video = cv2.VideoCapture(0)
        

    def __del__(self):
        self.video.release()

    def get_gray(self):
        success, image = self.video.read()
        _, jpeg = cv2.imencode('.jpg', image)
        return [jpeg.tobytes(), posture_output]
    
                                

    