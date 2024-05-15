import cv2
import numpy as np
import sqlite3
from face_recognition.models import Student
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Capture faces using webcam and update the database'

    def handle(self, *args, **options):
        faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        cam = cv2.VideoCapture(0)



        def insert_or_update(id, name, age):
            student, created = Student.objects.get_or_create(id=id)
            student.name = name
            student.age = age
            student.save()

   
   
# Insert user defined values into table
        Id = input('Enter User Id:')
        Name = input('Enter User Name:')
        age = input('Enter User age:')

        insert_or_update(Id, Name, age)

# Detect face in web camera coding

        sampleNum = 0
        while True:
          ret, img = cam.read()
          gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
          faces = faceDetect.detectMultiScale(gray, 1.3, 5)
          for (x, y, w, h) in faces:
               sample_num += 1
               cv2.imwrite(f"dataset/user.{id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
               cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0),2)
          cv2.imshow("Face", img)
          if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
              break
          if sampleNum > 40:
              break

        cam.release()
        cv2.destroyAllWindows()
