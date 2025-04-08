import os
import cv2
import sqlite3
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
API_URL = "https://detect.roboflow.com"
API_KEY = "vTd7sGLZDtRa0U3aTpeD"
FACE_MODEL_PATH = "EncodeFile.p"
detector = UniformViolationDetector(API_URL, API_KEY, FACE_MODEL_PATH)



def get_db_connection():
    """Establish and return a database connection."""
    conn = sqlite3.connect('database/student.db')
    conn.row_factory = sqlite3.Row
    return conn

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

# Office365 Email credentials
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

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


@app.route('/api/update_fine/<unique_id>', methods=['POST'])
def update_fine(unique_id):
    """Increase fine amount for a student."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE student_fine
            SET fine_amount = COALESCE(fine_amount, 0) + 50
            WHERE JNTU = ?;
        """, (unique_id,))

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"message": "Student ID not found"}), 404

        conn.commit()
        conn.close()
        return jsonify({"message": "Fine amount updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/students', methods=['GET'])
def get_all_students():
    """Retrieve all student fine records."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_fine;")
        rows = cursor.fetchall()
        students = [dict(row) for row in rows]
        conn.close()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
