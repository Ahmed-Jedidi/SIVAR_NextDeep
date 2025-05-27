import cv2
import time
from ultralytics import YOLO
from playsound import playsound


import pyttsx3
engine = pyttsx3.init()


from collections import deque
# Track frames for short-term video capture
frame_buffer = deque(maxlen=150)  # Store last ~5 seconds if 30 FPS


#***********************************************************## Import face recognition libraries
import face_recognition
import os
#***********************************************************#
known_face_encodings = []
known_face_names = []

for filename in os.listdir("known_faces"):
    image_path = os.path.join("known_faces", filename)
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if encodings:
        known_face_encodings.append(encodings[0])
        name = os.path.splitext(filename)[0]
        known_face_names.append(name)
#***********************************************************#

# Load YOLOv8 model (best balance: yolov8n.pt or yolov8s.pt)
model = YOLO("yolov8n.pt")  # Downloaded automatically on first run

# Initialize webcam
cap = cv2.VideoCapture(0)

# Define zone (x1, y1, x2, y2)
zone = (150, 100, 500, 400)
enter_time = None
alert_triggered = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

#############################################################""
    # Add to main loop:
    frame_buffer.append(frame.copy())
#############################################################""


    results = model(frame, verbose=False)
    person_in_zone = False

    for result in results:
        for box in result.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            if cls == 0 and conf > 0.5:  # Class 0 = person
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                person_center = ((x1 + x2) // 2, (y1 + y2) // 2)

                # Draw person bounding box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Check if person is inside zone
                zx1, zy1, zx2, zy2 = zone
                if zx1 < person_center[0] < zx2 and zy1 < person_center[1] < zy2:
                    person_in_zone = True

    # Time tracking
    if person_in_zone:
        if enter_time is None:
            enter_time = time.time()
        elif time.time() - enter_time > 2 and not alert_triggered:
            print("🚨 ALERT: Person in restricted area for over 30 seconds!")

            # Save screenshot
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"screenshot_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"📷 Screenshot saved as {filename}")
##***********************************************************#
#            # Crop the person's bounding box from YOLO
#            person_crop = frame[ymin:ymax, xmin:xmax]
#            rgb_person_crop = cv2.cvtColor(person_crop, cv2.COLOR_BGR2RGB)
#
#            face_locations = face_recognition.face_locations(rgb_person_crop)
#            face_encodings = face_recognition.face_encodings(rgb_person_crop, face_locations)
#
#            for face_encoding in face_encodings:
#                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
#                name = "Unknown"
#
#                if True in matches:
#                    match_index = matches.index(True)
#                    name = known_face_names[match_index]
#                    print(f"🎯 MATCHED: {name}")
#
#                    # Trigger 30s stay detection only for this person
#                    if name == "John":  # or your intruder’s name
#                        # Insert your timer and alert logic here
##***********************************************************#
            ####################################################################################""
            ## Start video recording
            #out = cv2.VideoWriter(f"alert_{timestamp}.avi",
            #                      cv2.VideoWriter_fourcc(*'XVID'), 30,
            #                      (frame.shape[1], frame.shape[0]))
#
            #print("🎥 Recording 10-second alert video...")
#
            ## Save buffered frames first
            #for buffered_frame in frame_buffer:
            #    out.write(buffered_frame)
#
            ## Record 5 more seconds live
            #start_time = time.time()
            #while time.time() - start_time < 5:
            #    ret, new_frame = cap.read()
            #    if not ret:
            #        break
            #    out.write(new_frame)
            #    cv2.imshow("Recording...", new_frame)
            #    if cv2.waitKey(1) & 0xFF == ord('q'):
            #        break
            #    
            #out.release()
            #print("✅ Video saved!")
            #####################################################################################""


            playsound("alert.mp3")  # Place alert.mp3 in the same folder
            engine.say("Warning. A person has been in the restricted area for more than 30 seconds.")
            engine.runAndWait()
            alert_triggered = True
            
    else:
        enter_time = None
        alert_triggered = False

    # Draw zone
    cv2.rectangle(frame, (zone[0], zone[1]), (zone[2], zone[3]), (0, 0, 255), 2)
    cv2.putText(frame, "Protected Zone", (zone[0], zone[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Display
    cv2.imshow("Intrusion Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
