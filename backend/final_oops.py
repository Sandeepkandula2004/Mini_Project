import os
import cv2
import numpy as np
from inference_sdk import InferenceHTTPClient
from face import FaceRecognition

class UniformViolationDetector:
    def __init__(self, api_url, api_key, face_model_path, output_dir="static/processed"):
        self.client = InferenceHTTPClient(api_url=api_url, api_key=api_key)
        self.face_recognition = FaceRecognition(face_model_path)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
    
    def detect_objects(self, image, model_id):
        result = self.client.infer(image, model_id=model_id)
        return result.get("predictions", [])

    def process_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or invalid format.")
        
        # Object detection
        result1 = self.detect_objects(image, model_id="id-fqivr/4")
        result2 = self.detect_objects(image, model_id="id-fqivr/2")
        
        detected_objects = set()
        student_ids = []

        # Draw bounding boxes for detected objects only if confidence >= 70%
        for prediction in result1 + result2:
            confidence = prediction["confidence"]
            if confidence < 0.7:  # Skip drawing if confidence < 70%
                continue

            px, py, pw, ph = int(prediction["x"]), int(prediction["y"]), int(prediction["width"]), int(prediction["height"])
            start_point, end_point = (px - pw // 2, py - ph // 2), (px + pw // 2, py + ph // 2)
            color = (0, 255, 0) if prediction in result1 else (255, 0, 0)
            cv2.rectangle(image, start_point, end_point, color, 2)
            label = f"{prediction['class']} ({confidence:.2f})"
            cv2.putText(image, label, (start_point[0], start_point[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Add to detected objects
            detected_objects.add(prediction["class"])

        # Check for uniform violations
        if "BLACK_SHOES" not in detected_objects or "ID_CARD" not in detected_objects:
            recognized_faces = self.face_recognition.recognize_faces(image)
            for (fx, fy, fw, fh, name) in recognized_faces:
                cv2.rectangle(image, (fx, fy), (fx+fw, fy+fh), (0, 0, 255), 2)
                cv2.putText(image, name, (fx, fy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                student_ids.append(name)

        # Save output image
        output_path = os.path.join(self.output_dir, "output.jpg")
        cv2.imwrite(output_path, image)
        
        return output_path, student_ids
