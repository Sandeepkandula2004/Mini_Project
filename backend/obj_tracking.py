import cv2
from ultralytics import YOLO

# Load the YOLOv11 model
model = YOLO("yolo11n.pt")  # Replace with the path to your YOLOv11 model

# Initialize webcam capture
cap = cv2.VideoCapture(0)  # Change to 1 for external webcam

# Get webcam properties (optional)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Perform object detection and tracking
    results = model.track(frame)

    # Draw bounding boxes and labels
    annotated_frame = results[0].plot()

    

    # Display the frame
    cv2.imshow('YOLOv11 Object Tracking (Webcam)', annotated_frame)



    # Exit if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()