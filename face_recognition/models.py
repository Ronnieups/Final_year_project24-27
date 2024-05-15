import cv2
from django.db import models

class Student(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit id field
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    age = models.IntegerField()
    parent_contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class PickupPerson(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    nin = models.CharField(max_length=20, unique=True)  # National Identification Number
    contact = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='pickup_person_photos')

    def __str__(self):
        return self.name

class FaceRegistration(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit id field
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pickup_person = models.ForeignKey(PickupPerson, on_delete=models.CASCADE)
    face_data = models.TextField()  # For storing encoded face data

    def recognize_face(self, face_image_path):
        # Load the face recognition model
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("recognizer/trainingdata.yml")

        # Load the face cascade classifier
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        # Read the image and convert it to grayscale
        img = cv2.imread(face_image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Recognize faces and return the recognized IDs and confidences
        recognized_faces = []
        for (x, y, w, h) in faces:
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            recognized_faces.append((id, confidence))
        return recognized_faces

    def __str__(self):
        return f"{self.student.name} - {self.pickup_person.name}"

class PickupSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pickup_person = models.ForeignKey(PickupPerson, on_delete=models.CASCADE)
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"{self.student.name} - {self.pickup_person.name} at {self.pickup_time}"

class PickupLog(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    pickup_person = models.ForeignKey(PickupPerson, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} picked up by {self.pickup_person.name} on {self.timestamp}"