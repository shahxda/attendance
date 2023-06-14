from flask import Flask, render_template, request, redirect
import cv2
import face_recognition
import csv
import numpy as np
from datetime import datetime
import os
from flask import url_for, redirect  

app = Flask(__name__)

# ----------- Module 1 (Manipulation of Input data) -------------
# Run-time database for recording attendance (dictionary)
attendance_db = {}

# Make a list to hold attendance data
attendance_info = []

# Path of the folder containing known images
img_folder = "/Users/3hood/Desktop/attendance 2 2/FACE"

# Get a list of image files that exist in the img folder
img_files = os.listdir(img_folder)

# Creating lists of images and their respective names
# Listing paths of given images
given_imgs = [os.path.join(img_folder, file) for file in img_files]
# Getting img file's labels as names
given_names = [os.path.splitext(file)[0] for file in img_files]

# Get encodings of given faces (images)
known_images_encodings = []
for img_path in given_imgs:
    img = face_recognition.load_image_file(img_path)
    encoding = face_recognition.face_encodings(img)[0]
    known_images_encodings.append(encoding)

def run_face_recognition():
    # Perform the face recognition logic here

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

                    # Updating attendance db on runtime
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
    print("\n[INFO] Attendance Data:")
    print("=========================================")
    print("  Name\t\t|\tTime of Arrival")
    print("-----------------------------------------")
    for info in attendance_info:
        print(f"  {info[0]}\t|\t{info[1]}")
    print("=========================================")

    # --------- Writing attendance data to CSV file ----------
    # Create a directory named 'output' to store attendance data
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set the filename to the current date and time
    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

    # Write attendance data to the CSV file
    with open(os.path.join(output_dir, filename), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Time of Arrival"])
        writer.writerows(attendance_info)
 
    # Redirect to the summary page after face recognition is complete
    student_id = request.form['studentID']
    summary_url = url_for('summary', student_id=student_id)
    return redirect(summary_url)


# ----------- Module 2 (Checking faces in real time) -------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/face_recognition', methods=['POST'])
def face_recognition_route():
    return run_face_recognition()


# ----------- Module 3 (Routing and Rendering) -------------
if __name__ == '__main__':
    app.run()



