import cv2
import face_recognition
import pickle

class FaceRecognition:
    def __init__(self, encode_file_path):
        """
        Initialize the FaceRecognition system by loading encodings and IDs.
        """
        with open(encode_file_path, 'rb') as file:
            encode_list_known_with_ids = pickle.load(file)
        
        self.encode_list_known, self.student_ids = encode_list_known_with_ids
        self.video_capture = cv2.VideoCapture(0)
        print("Face Recognition system initialized.")

    def detect_faces(self):
        """
        Start the face recognition process.
        Returns a list of detected student IDs.
        """
        detected_students = []

        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                print("Failed to capture frame.")
                break

            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect faces and encode them
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(self.encode_list_known, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(self.encode_list_known, face_encoding)
                best_match_index = face_distances.argmin() if matches else None

                name = "Unknown"
                if best_match_index is not None and matches[best_match_index]:
                    name = self.student_ids[best_match_index]
                    detected_students.append(name)

                # Draw a rectangle around the face
                top, right, bottom, left = face_location
                top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            cv2.imshow("Video", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video_capture.release()
        cv2.destroyAllWindows()
        return detected_students

if __name__ == "__main__":
    # Path to the encoded file
    encode_file_path = "EncodeFile.p"

    # Create an instance of FaceRecognition
    face_recognition_system = FaceRecognition(encode_file_path)

    # Start detecting faces and get the detected student IDs
    print("Starting Face Recognition...")
    detected_students = face_recognition_system.detect_faces()

    print("Detected Students:", detected_students)
