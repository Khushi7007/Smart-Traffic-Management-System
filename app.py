from flask import Flask, render_template
from ultralytics import YOLO
import cv2

app = Flask(__name__)


model = YOLO("yolov8n.pt")


cap = cv2.VideoCapture("traffic.mp4")

@app.route('/')
def home():

    global cap

    ret, frame = cap.read()


    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

    results = model(frame)

    vehicle_count = 0

    for box in results[0].boxes:

        cls = int(box.cls[0])

        if cls in [2, 3, 5, 7]:
            vehicle_count += 1

    
    if vehicle_count > 40:
        signal = "GREEN"
        green_time = 60

    elif vehicle_count > 20:
        signal = "YELLOW"
        green_time = 40

    else:
        signal = "RED"
        green_time = 20

    return render_template(
        'index.html',
        vehicle_count=vehicle_count,
        signal=signal,
        green_time=green_time
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=1239)