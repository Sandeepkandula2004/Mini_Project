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
                    x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                    
                    # Extract face region
                    face_crop = image[y:y+h, x:x+w]
                    face_crop = cv2.resize(face_crop, (150, 150))
                    face_crop_rgb = cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB)
                    
                    # Get face encoding
                    face_encoding = face_recognition.face_encodings(face_crop_rgb)
                    name = "Unknown"
                    
                    if face_encoding:
                        face_encoding = face_encoding[0]
                        matches = face_recognition.compare_faces(self.encode_list_known, face_encoding, tolerance=0.6)
                        face_distances = face_recognition.face_distance(self.encode_list_known, face_encoding)
                        best_match_index = face_distances.argmin() if matches else None
                        
                        if best_match_index is not None and matches[best_match_index]:
                            name = self.student_ids[best_match_index]
                    
                    recognized_faces.append((x, y, w, h, name))
        
        return recognized_faces