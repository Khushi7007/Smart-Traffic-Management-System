from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")


cap = cv2.VideoCapture("traffic.mp4")

while True:

    ret, frame = cap.read()

    if not ret:
        break


    results = model(frame)

    vehicle_count = 0

    
    for box in results[0].boxes:

        cls = int(box.cls[0])

        
        if cls in [2, 3, 5, 7]:
            vehicle_count += 1

    
    
    

    if vehicle_count > 40:
        green_time = 60
        signal = "GREEN"

    elif vehicle_count > 20:
        green_time = 40
        signal = "YELLOW"

    else:
        green_time = 20
        signal = "RED"

    
    
    lane1_count = vehicle_count // 2
    lane2_count = vehicle_count - lane1_count

    if lane1_count > lane2_count:
        lane1_green = 50
        lane2_green = 20

    else:
        lane1_green = 20
        lane2_green = 50

    
    annotated = results[0].plot()

    
    
    
    cv2.putText(annotated,
                f"Vehicles: {vehicle_count}",
                (20,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,0),
                2)

    
    cv2.putText(annotated,
                f"Green Time: {green_time}s",
                (20,100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,0,0),
                2)

    
    cv2.putText(annotated,
                f"Signal: {signal}",
                (20,150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,0,255),
                2)

    
    cv2.putText(annotated,
                f"Lane1: {lane1_count} vehicles",
                (20,200),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,0),
                2)

    cv2.putText(annotated,
                f"Lane2: {lane2_count} vehicles",
                (20,250),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,0),
                2)

    # Lane green timings
    cv2.putText(annotated,
                f"Lane1 Green: {lane1_green}s",
                (20,300),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,255),
                2)

    cv2.putText(annotated,
                f"Lane2 Green: {lane2_green}s",
                (20,350),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0,255,255),
                2)

    
    cv2.imshow("Smart Traffic Management System", annotated)

    
    if cv2.waitKey(1) == 27:
        break


cap.release()
cv2.destroyAllWindows()