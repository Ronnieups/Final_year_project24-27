import cv2
import numpy as np
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PickupPersonForm, FaceRegistrationForm
from .models import PickupPerson, FaceRegistration, PickupSchedule, Student, PickupLog

def dashboard(request):
    return render(request, 'staff/dashboard.html')

def register_pickup_person(request):
    if request.method == 'POST':
        form = PickupPersonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PickupPersonForm()
    return render(request, 'staff/register_pickup_person.html', {'form': form})

def recognize_faces(image):
    # Load pre-trained face recognition model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("path_to_trained_model.yml")

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Recognize the face
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        # Check if confidence is within a certain threshold
        if confidence < 50:
            # Face recognized, perform further actions
            # For example, you can get the student corresponding to the recognized face
            student = Student.objects.get(id=id)
            return student
        else:
            # Face not recognized
            return None

def register_face(request):
    if request.method == 'POST':
        form = FaceRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the uploaded image
            uploaded_image = request.FILES['image']
            nparr = np.fromstring(uploaded_image.read(), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Recognize faces in the uploaded image
            recognized_student = recognize_faces(image)
            if recognized_student:
                messages.success(request, f"Face recognized: {recognized_student.name}")
            else:
                messages.warning(request, "Face not recognized")

            return redirect('dashboard')
    else:
        form = FaceRegistrationForm()
    return render(request, 'staff/register_face.html', {'form': form})
def pickup_schedule(request):
    pickup_schedule = PickupSchedule.objects.all()
    return render(request, 'staff/pickup_schedule.html', {'pickup_schedule': pickup_schedule})

def log_pickup(student_id, pickup_person_id):
    student = Student.objects.get(id=student_id)
    pickup_person = PickupPerson.objects.get(id=pickup_person_id)
    PickupLog.objects.create(student=student, pickup_person=pickup_person)
    # Here, add code to send SMS notification to parent
