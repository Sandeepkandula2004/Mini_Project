import cv2
import pickle
import mediapipe as mp
import face_recognition

class FaceRecognition:
    def __init__(self, encode_file_path):
        with open(encode_file_path, 'rb') as file:
            self.encode_list_known, self.student_ids = pickle.load(file)
        self.mp_face_detection = mp.solutions.face_detection
    
    def recognize_faces(self, image):
        recognized_faces = []

        with self.mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image_rgb)

            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = image.shape
                    x = int(bboxC.xmin * iw)
                    y = int(bboxC.ymin * ih)
                    w = int(bboxC.width * iw)
                    h = int(bboxC.height * ih)

                    # Ensure bounding box is within image bounds
                    x1 = max(0, x)
                    y1 = max(0, y)
                    x2 = min(iw, x + w)
                    y2 = min(ih, y + h)

                    face_crop = image[y1:y2, x1:x2]

                    # Skip invalid or very small crops
                    if face_crop.size == 0 or face_crop.shape[0] < 10 or face_crop.shape[1] < 10:
                        continue

                    # Resize and convert
                    face_crop = cv2.resize(face_crop, (150, 150))
                    face_crop_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                    face_crop_rgb = face_crop_rgb.astype('uint8')  # Ensure correct type

                    # Get face encoding
                    name = "Unknown"
                    face_encoding = face_recognition.face_encodings(face_crop_rgb)

                    if face_encoding:
                        face_encoding = face_encoding[0]
                        matches = face_recognition.compare_faces(self.encode_list_known, face_encoding, tolerance=0.6)
                        face_distances = face_recognition.face_distance(self.encode_list_known, face_encoding)
                        best_match_index = face_distances.argmin() if matches else None

                        if best_match_index is not None and matches[best_match_index]:
                            name = self.student_ids[best_match_index]

                    recognized_faces.append((x, y, w, h, name))

        return recognized_faces


# import pickle

# with open("EncodeFile.p", "rb") as f:
#     data = pickle.load(f)

# print("✅ Type of data:", type(data))         # Should be <class 'tuple'>
# print("✅ Length of tuple:", len(data))       # Should be 2
# print("✅ Type of first element:", type(data[0]))  # Should be list (encodings)
# print("✅ Type of second element:", type(data[1])) # Should be list (IDs)

# # Sanity check
# print("✅ Number of known encodings:", len(data[0]))
# print("✅ Sample student ID:", data[1][0])
