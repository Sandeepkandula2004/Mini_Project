import os
import cv2
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from final_oops import UniformViolationDetector
from concurrent.futures import ThreadPoolExecutor
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv()

executor = ThreadPoolExecutor()
app = Flask(__name__)
CORS(app)

# Create required directories
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed_images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# API Configuration
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")
FACE_MODEL_PATH = "EncodeFile.p"
detector = UniformViolationDetector(API_URL, API_KEY, FACE_MODEL_PATH)

# MongoDB Configuration
from urllib.parse import quote_plus
MONGO_USER = os.getenv("MONGO_USER", "sandeep")
mongo_password = quote_plus(os.getenv("MONGO_PASS")) 
MONGO_URI = f"mongodb+srv://sandeep:{mongo_password}@cluster0.d94uq9i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["my_database"]
student_fine_collection = db["student_fine"]

# Office365 Email credentials
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

# Function to update fines

def update_fines(detected_face_ids):
    """Update fines for detected students."""
    updated_students = []
    detected_face_ids = set(detected_face_ids)

    for face_id in detected_face_ids:
        try:
            response = requests.post(f'http://127.0.0.1:5000/api/update_fine/{face_id}', timeout=5)
            if response.status_code == 200:
                updated_students.append(face_id)
        except requests.exceptions.RequestException as e:
            print(f"Failed to update fine for {face_id}: {str(e)}")

    print("Fines updated for:", updated_students)

# Send email

def send_violation_email(student_ids):
    """Send email notifications for uniform violations using Office365 SMTP."""
    subject = "Uniform Violation Detected"
    sanitized_ids = [student_id.strip() for student_id in student_ids]
    body = f"You have uniform violations: {', '.join(sanitized_ids)}."
    recipient_emails = [f"{student_id}@gmrit.edu.in" for student_id in sanitized_ids]

    for student_id, recipient in zip(sanitized_ids, recipient_emails):
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP("smtp.office365.com", 587)
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, recipient, msg.as_string())
            server.quit()

            print(f"✅ Email sent successfully to {recipient} (ID: {student_id})")
        except Exception:
            pass  # You can replace this with logging to a file if needed

# Process image
@app.route('/api/process', methods=['POST'])
def process_image():
    """Process an uploaded image and detect uniform violations."""
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    try:
        # Process the image using the detector
        output_path, detected_face_ids = detector.process_image(filename)

        if detected_face_ids:
            update_fines(detected_face_ids)

            # Send email in the background
            executor.submit(send_violation_email, detected_face_ids)

        return jsonify({
            "detected_face_ids": detected_face_ids,
            "processed_image": output_path
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update fine
@app.route('/api/update_fine/<unique_id>', methods=['POST'])
def update_fine(unique_id):
    """Increase fine amount for a student."""
    try:
        result = student_fine_collection.update_one(
            {"JNTU": unique_id},
            {"$inc": {"fine_amount": 50}}
        )

        if result.matched_count == 0:
            return jsonify({"message": "Student ID not found"}), 404

        return jsonify({"message": "Fine amount updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students', methods=['GET'])
def get_all_students():
    """Retrieve all student fine records."""
    try:
        students = list(student_fine_collection.find({}, {"_id": 0}))
        return jsonify(students), 200
    except Exception as e:
        print("Error in /api/students:", e)  # <--- Add this
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
