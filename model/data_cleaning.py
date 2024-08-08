import os
import numpy as np
import pywt
import cv2   
import shutil
import sys


def get_cropped_image_if_2_eyes(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >= 2:
            return roi_color



path_to_data = "./dataset/"
path_to_cr_data = "./dataset/cropped/"

img_dirs = []
for entry in os.scandir(path_to_data):
    if entry.is_dir():
        img_dirs.append(entry.path)

if os.path.exists(path_to_cr_data):
     shutil.rmtree(path_to_cr_data)
os.mkdir(path_to_cr_data)

cropped_image_dirs = []

for img_dir in img_dirs:
    count = 1 
    celebrity_name = img_dir.split('/')[-1]
    for entry in os.scandir(img_dir):
        if entry.path.split('.')[-1] in ['jpeg','jpg','png','bmp','tiff','tif','webp']:
            roi_color = get_cropped_image_if_2_eyes(entry.path)
            if roi_color is not None:
                cropped_folder = path_to_cr_data + celebrity_name
                if not os.path.exists(cropped_folder):
                    # Crée un chemin de répertoires de manière récursive même si les répertoires parents n'existent pas, os.makedirs les créera automatiquement.
                    os.makedirs(cropped_folder)
                    cropped_image_dirs.append(cropped_folder)
                cropped_file_name = celebrity_name + str(count) + ".png"
                cropped_file_path = cropped_folder + "/" + cropped_file_name
                cv2.imwrite(cropped_file_path, roi_color)
                count += 1




