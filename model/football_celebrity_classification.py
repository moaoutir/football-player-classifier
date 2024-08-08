from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

import os
import cv2
import numpy as np
import sys
import joblib
import json

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import wavelet

path_to_cr_data = "./dataset/cropped/"
cropped_image_dirs = []
for entry in os.scandir(path_to_cr_data):
    if entry.is_dir():
        cropped_image_dirs.append(entry.path)

celebrity_file_names_dict = {}
for img_dir in cropped_image_dirs:
    celebrity_name = img_dir.split('/')[-1]
    img_list = []
    for entry in os.scandir(img_dir):
        img_list.append(entry.path)
    celebrity_file_names_dict[celebrity_name] = img_list

class_dict = {}
count = 0
for celebrity_name in celebrity_file_names_dict.keys():
    class_dict[celebrity_name] = count
    count += 1

X, y = [], []
for celebrity_name, training_files in celebrity_file_names_dict.items():
    for training_image in training_files:
        img = cv2.imread(training_image)
        scalled_raw_img = cv2.resize(img, (32, 32))
        img_har = wavelet.w2d(img,'db1',5)
        scalled_img_har = cv2.resize(img_har, (32, 32))
        combined_img = np.vstack((scalled_raw_img.reshape(32*32*3,1),scalled_img_har.reshape(32*32,1)))
        X.append(combined_img)
        y.append(class_dict[celebrity_name])    

# 32*32*3 + 32*32 = 4096            
X = np.array(X).reshape(len(X),4096).astype(float)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])
param_grid = {
    'classifier__solver':['liblinear','lbfgs'],
    'classifier__C': [0.1,0.5,1,5,10],
    'classifier__penalty': ['l2']
}


grid = GridSearchCV(pipeline, param_grid, cv=5, return_train_score=False)
grid.fit(X_train, y_train)
print(grid.best_params_)
print(grid.best_score_)


joblib.dump(grid, '../server/artifacts/saved_model.pkl') 

with open("../server/artifacts/class_dictionary.json","w") as f:
    f.write(json.dumps(class_dict))