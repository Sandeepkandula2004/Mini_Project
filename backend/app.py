from flask import Flask, request, jsonify, Response
import sqlite3
import requests
from flask_cors import CORS
import cv2
from uniOOPS1 import UniformDetection
import os
app = Flask(__name__)
CORS(app)

encode_file_path = "EncodeFile.p" 
model_path = "yolo11n.pt"
uniform_detection = UniformDetection(model_path, encode_file_path)

detected_face_ids = []
streaming = False  # Track if streaming is active

def generate_frames():
    global detected_face_ids, streaming
    cap = cv2.VideoCapture(0)
    detected_face_ids = []
    streaming = True  # Start streaming

    while streaming:
        success, frame = cap.read()
        if not success:
            break

        processed_frame, face_ids = uniform_detection.process_frame(frame)
        detected_face_ids.extend(face_ids)

        _, buffer = cv2.imencode(".jpg", processed_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
    update_fines_after_stream()


def update_fines_after_stream():
    """Update fines after streaming ends"""
    global detected_face_ids
    updated_students = []
    detected_face_ids = set(detected_face_ids)
    for face_id in detected_face_ids:
        try:
            response = requests.post(f'http://127.0.0.1:5000/api/update_fine/{face_id}', timeout=5)
            if response.status_code == 200:
                updated_students.append(face_id)
        except requests.exceptions.RequestException:
            continue

    print("Fines updated for:", updated_students)
    detected_face_ids.clear()  # Clear after updating

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def update_fines(detected_face_ids):
    """Update fines for detected students"""
    updated_students = []
    detected_face_ids = set(detected_face_ids)
    for face_id in detected_face_ids:
        try:
            response = requests.post(f'http://127.0.0.1:5000/api/update_fine/{face_id}', timeout=5)
            if response.status_code == 200:
                updated_students.append(face_id)
        except requests.exceptions.RequestException:
            continue
    print("Fines updated for:", updated_students)

def process_video(file_path):
    """Processes the uploaded video for face detection and saves processed frames."""
    detected_face_ids = []
    cap = cv2.VideoCapture(file_path)
    
    processed_video_path = os.path.join(PROCESSED_FOLDER, os.path.basename(file_path))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None
    
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        processed_frame, face_ids = uniform_detection.process_frame(frame)
        detected_face_ids.extend(face_ids)
        
        if out is None:
            height, width, _ = processed_frame.shape
            out = cv2.VideoWriter(processed_video_path, fourcc, 20.0, (width, height))
        
        out.write(processed_frame)
    
    cap.release()
    if out:
        out.release()
    
    update_fines(detected_face_ids)
    return list(set(detected_face_ids))

@app.route("/api/upload_video", methods=["POST"])
def upload_video():
    """Handles video file upload and processes it for face detection."""
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400
    
    video_file = request.files["video"]
    file_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(file_path)
    
    detected_faces = process_video(file_path)
    return jsonify({"message": "Video processed successfully", "detected_faces": detected_faces}), 200

@app.route("/video_feed")
def video_feed():
    """Streams video feed from the webcam"""
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/api/stop_stream", methods=["POST"])
def stop_stream():
    global streaming
    streaming = False  # Stop streaming
    return jsonify({"message": "Streaming stopped"}), 200

def get_db_connection():
    """Establish and return a database connection"""
    conn = sqlite3.connect('database/student.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/update_fine/<unique_id>', methods=['POST'])
def update_fine(unique_id):
    """Increase fine amount for a student"""
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
    """Retrieve all student fine records"""
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
