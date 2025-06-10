import cv2
import numpy as np
from ultralytics import YOLO
import cvzone
import time
import os
import subprocess

# Set up the OpenCV window
cv2.namedWindow('Helmet Detection System')

# Clear YOLO cache directory to avoid conflicts
cache_dir = os.path.expanduser("~/.cache/ultralytics")
if os.path.exists(cache_dir):
    for root, dirs, files in os.walk(cache_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    print("Previous cache cleared.")

# Load the YOLOv8 model
model = YOLO("c:/Users/Asus/Desktop/website/best.pt")
names = model.model.names

# Open the video file (use video file or webcam; here, using webcam)
cap = cv2.VideoCapture(0)

# Initialize FPS tracking
fps_start_time = time.time()
frame_count = 0

# NMS threshold
nms_threshold = 0.9

# Start simulator
simulator_process = None

# Track helmet detection status
helmet_detected_time = None
helmet_not_detected_threshold = 10  # Seconds before sending 'X'

# Path to the text file that will indicate "X" key press
file_path = "simulator_command.txt"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Increment frame count
    frame_count += 1

    # Resize the frame for better FPS
    frame = cv2.resize(frame, (440, 440))

    # Run YOLOv8 detection
    results = model.track(frame, persist=True)

    # Check if there are any detections
    helmet_detected = False
    if results[0].boxes is not None and results[0].boxes.id is not None:
        # Get the boxes (x, y, w, h), class IDs, track IDs, and confidences
        boxes = results[0].boxes.xyxy.cpu().numpy()  # Bounding boxes
        class_ids = results[0].boxes.cls.int().cpu().tolist()  # Class IDs
        confidences = results[0].boxes.conf.cpu().tolist()  # Confidence scores

        # Apply Non-Maximum Suppression (NMS)
        indices = cv2.dnn.NMSBoxes(
            boxes.tolist(),
            confidences,
            score_threshold=0.6,  # Confidence threshold
            nms_threshold=nms_threshold
        )

        if len(indices) > 0:
            for i in indices.flatten():
                x1, y1, x2, y2 = map(int, boxes[i])
                class_id = class_ids[i]
                conf = confidences[i]
                label = names[class_id]

                # Check if helmet is detected
                if label == "helmet" and conf > 0.6:
                    helmet_detected = True
                    helmet_detected_time = time.time()  # Reset the timer if helmet is detected

                    if simulator_process is None:
                        # Start the simulator when helmet is first detected
                        simulator_process = subprocess.Popen(["python", "simulator.py"])

                # Draw the bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (139, 0, 0), 2)
                # Display class and confidence
                cvzone.putTextRect(frame, f'{label} ({conf:.2f})', (x1, y1), 1, 1, colorT=(255, 255, 255), colorR=(0, 0, 0))

    # If no helmet detected for the specified threshold, write "X" to the text file
    if helmet_detected_time and time.time() - helmet_detected_time > helmet_not_detected_threshold:
        if simulator_process and simulator_process.poll() is None:  # Check if simulator is running
            with open(file_path, "w") as f:
                f.write("X")  # Simulate "X" key press in the simulator
            print("Written 'X' to the text file.")
            helmet_detected_time = None  # Reset the timer

    # Show the frame
    cv2.imshow("Helmet Detection System", frame)

    # Press 'q' to quit the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
