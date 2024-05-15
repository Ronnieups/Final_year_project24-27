import cv2
import numpy as np
import os
from face_recognition.models import Student
#import sqlite3

faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("recognizer/trainingdata.yml")


def get_profile(id):
    try:
        student = Student.objects.get(id=id)
        return (student.id, student.name, student.age)
    except Student.DoesNotExist:
        return None
  # conn = sqlite3.connect("sqlite.db")
   # cursor = conn.execute("SELECT * FROM STUDENTS WHERE id=?", (id,))
   # profile = cursor.fetchone()  # Fetch only one row
   # conn.close()
    #return profile


while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceDetect.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, conf = recognizer.predict(gray[y:y + h, x:x + w])
        print("Recognized ID:", id)
        profile = get_profile(id)
        if profile is not None:
            print("Profile:", profile)
            cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127),
                        2)
            cv2.putText(img, "Age: " + str(profile[2]), (x, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127),
                        2)

    cv2.imshow("FACE", img)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
