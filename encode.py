import cv2
import face_recognition
import pickle
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

# Define the parent folder containing class folders
parentFolderPath = 'images'

if not os.path.exists(parentFolderPath):
    raise FileNotFoundError(f"Folder '{parentFolderPath}' does not exist.")

encodeListKnown = []
classNames = []

for classFolder in os.listdir(parentFolderPath):
    classFolderPath = os.path.join(parentFolderPath, classFolder)

    if not os.path.isdir(classFolderPath):
        continue

    images = [os.path.join(classFolderPath, img) for img in os.listdir(classFolderPath) if img.endswith(('.jpg', '.jpeg', '.png'))]

    print(f"Processing class: {classFolder} with {len(images)} images")

    for imgPath in tqdm(images, desc=f"Encoding {classFolder}"):
        img = cv2.imread(imgPath)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Detect face locations first
        face_locations = face_recognition.face_locations(img, model='hog')
        if face_locations:
            encodes = face_recognition.face_encodings(img, known_face_locations=face_locations)
            encodeListKnown.append(encodes[0])
            classNames.append(classFolder)
        else:
            print(f"No face found in image {imgPath}")
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            plt.title(f"No face detected in {imgPath}")
            plt.show()

encodeListKnownWithIds = [encodeListKnown, classNames]
print("Encoding Complete")

with open("EncodeFile.p", 'wb') as file:
    pickle.dump(encodeListKnownWithIds, file)

print("File Saved")
