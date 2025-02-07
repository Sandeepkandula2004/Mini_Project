import cv2
import requests
import numpy as np
import face_recognition
import pickle
from ultralytics import YOLO

class UniformDetection:
    API_URL = "https://detect.roboflow.com/university-uniform-detection/2"
    API_KEY = "g2CNedqJbFmFZJ1UiQzf"
    EXCLUDED_CLASSES = {"uniform-top", "uniform-bottom", "uniform-logo"}

    def __init__(self, model_path, encode_file_path):
        self.model = YOLO(model_path)
        self.tracked_objects = {}
        self.detected_face_ids = []  # List to store detected face IDs

        # Load face encodings
        with open(encode_file_path, 'rb') as file:
            encode_list_known_with_ids = pickle.load(file)
        self.encode_list_known, self.student_ids = encode_list_known_with_ids

    def detect_objects(self, frame):
        return self.model.track(frame)

    def query_roboflow(self, image):
        _, img_encoded = cv2.imencode('.jpg', image)
        response = requests.post(
            f"{self.API_URL}?api_key={self.API_KEY}",
            files={"file": img_encoded.tobytes()}
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error querying Roboflow: {response.status_code} - {response.text}")
            return None

    def query_face_model(self, image):
        # Resize image for face recognition
        small_frame = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces and encode them
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_ids = []
        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(self.encode_list_known, face_encoding, tolerance=0.6)
            face_distances = face_recognition.face_distance(self.encode_list_known, face_encoding)
            best_match_index = face_distances.argmin() if matches else None

            face_id = "Unknown"
            if best_match_index is not None and matches[best_match_index]:
                face_id = self.student_ids[best_match_index]
                face_ids.append((face_id, face_location))

        return face_ids

    def draw_roboflow_boxes(self, frame, predictions, offset=(0, 0)):
        x_offset, y_offset = offset
        for prediction in predictions:
            label = prediction["class"]
            if label in self.EXCLUDED_CLASSES:
                continue

            x1 = int(prediction["x"] - prediction["width"] / 2) + x_offset
            y1 = int(prediction["y"] - prediction["height"] / 2) + y_offset
            x2 = int(prediction["x"] + prediction["width"] / 2) + x_offset
            y2 = int(prediction["y"] + prediction["height"] / 2) + y_offset

            confidence = prediction["confidence"]

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(
                frame,
                f"{label}: {confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                2,
            )

    def process_frame(self, frame, results):
        for result in results:
            for box, cls, obj_id in zip(result.boxes.xyxy, result.boxes.cls, result.boxes.id):
                if int(cls) == 0:  # Class 0 is typically 'person'
                    x1, y1, x2, y2 = map(int, box)

                    self.tracked_objects[obj_id] = (x1, y1, x2, y2)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(
                        frame,
                        f"Person ID: {int(obj_id)}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2,
                    )

                    person_crop = frame[y1:y2, x1:x2]

                    if person_crop.size == 0:
                        continue

                    roboflow_result = self.query_roboflow(person_crop)

                    detected_classes = set()
                    if roboflow_result and roboflow_result.get("predictions"):
                        predictions = roboflow_result["predictions"]
                        self.draw_roboflow_boxes(frame, predictions, offset=(x1, y1))
                        detected_classes = {pred["class"] for pred in predictions}

                    if not roboflow_result or "uniform-id" not in detected_classes or "uniform-shoes" not in detected_classes:
                        face_ids = self.query_face_model(person_crop)
                        for face_id, face_location in face_ids:
                            self.detected_face_ids.append(face_id)  # Collect face IDs
                            top, right, bottom, left = face_location
                            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
                            cv2.rectangle(frame, (x1 + left, y1 + top), (x1 + right, y1 + bottom), (0, 0, 255), 2)
                            cv2.putText(
                                frame,
                                f"Face ID: {face_id}",
                                (x1 + left, y1 + top - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                (0, 0, 255),
                                2,
                            )

        self.cleanup_tracked_objects()
        return frame

    def cleanup_tracked_objects(self):
        # Placeholder to remove lost objects if needed (e.g., based on custom logic)
        # This can include removing objects not updated for several frames
        pass

    def process_video(self, video_source):
        cap = cv2.VideoCapture(video_source)

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            resized_frame = cv2.resize(frame, (640, 480))
            results = self.detect_objects(resized_frame)

            processed_frame = self.process_frame(resized_frame, results)

            cv2.imshow('Uniform Detection', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return list(set(self.detected_face_ids))  # Return detected face IDs
    

if __name__ == "__main__":
    model_path = "yolo11n.pt"
    encode_file_path = "EncodeFile.p"

    print("Enter '0' for webcam or provide video file path:")
    video_source = input().strip()

    if video_source.isdigit():
        video_source = int(video_source)
        if video_source == 0:
            video_source = 0
        else:
            video_source = r"..\videos\videoplayback.mp4"

    uniform_detection = UniformDetection(model_path, encode_file_path)
    detected_face_ids = uniform_detection.process_video(video_source)
    print("Detected Face IDs:", detected_face_ids)
