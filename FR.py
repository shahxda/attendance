import cv2
import face_recognition
import csv
import numpy as np
from datetime import datetime
import os

# ----------- Module 1 (Manipulation of Input data) -------------

# run-time database for recording attendance (dictionary)
attendance_db = {}

# make list to hold attendance data
attendance_info = []

# Path of the folder containing known images
img_folder = "/Users/3hood/Desktop/attendance 2 2/FACE"

# Get list of image files that exist in the img folder
img_files = os.listdir(img_folder)

# Creating lists of images and their respective names
# Listing paths of given images
given_imgs = [os.path.join(img_folder, file) for file in img_files]
# Getting image file's labels as names
given_names = [os.path.splitext(file)[0] for file in img_files]

# Get encodings of given faces (images)
known_images_encodings = []
for img_path in given_imgs:
    img = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(img)[0]
    known_images_encodings.append(encoding)

# --------------------------------------------------------------------------------
# ------------------ Module 2 (Checking faces in real time) ----------------------

# Start video capture
vid_cap = cv2.VideoCapture(0)

# Go through video frames to compare given faces with faces on camera
while True:
    # Reading data from video capture frames
    r, frame = vid_cap.read()
    rgb_frame_var = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locs = face_recognition.face_locations(rgb_frame_var)

    # If there is at least one face
    if len(face_locs) > 0:
        face_encodings = face_recognition.face_encodings(rgb_frame_var, face_locs)

        # Comparing encodings of known faces with faces captured by camera frame
        for face_encode, face_loc in zip(face_encodings, face_locs):
            face_matches = face_recognition.compare_faces(known_images_encodings, face_encode)
            name = "unidentified"

            # If a face matches, then it checks for name and assigns it
            if True in face_matches:
                face_match_index = face_matches.index(True)
                name = given_names[face_match_index]

                # Updating attendance database on runtime
                if name not in attendance_db:
                    attendance_db[name] = datetime.now().strftime("%H:%M:%S")
                    attendance_info.append([name, attendance_db[name]])

            # Create a small rectangle on face detected in camera with a label (name of recognized face)
            t, r, b, l = face_loc
            cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
            cv2.putText(frame, name, (l, t - 10), cv2.FONT_HERSHEY_PLAIN, 0.9, (255, 0, 0), 2)

    cv2.imshow('Video', frame)

    # Turn off camera when 'x' is pressed
    if (cv2.waitKey(1) & 0xFF == ord('x')):
        break

# Closes camera window
vid_cap.release()
cv2.destroyAllWindows()

# --------- Simply printing attendance data onto the output terminal ----------
print("Attendance:")
for p_name, time in attendance_db.items():
    print(p_name, ":", time)

# ----------------------------------------------------------------------------
# ------- Module 3 (Creating a CSV file to record attendance data) -----------

# Getting location of folder where the code file exists to create a CSV file there
file_loc = os.path.join(os.getcwd(), datetime.now().strftime("%Y-%m-%d") + ".csv")

# Saving data into CSV file
with open(file_loc, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Time"])
    writer.writerows(attendance_info)
