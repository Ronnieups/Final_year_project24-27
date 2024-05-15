from django import forms
from .models import PickupPerson, FaceRegistration,PickupSchedule

class PickupPersonForm(forms.ModelForm):
    class Meta:
        model = PickupPerson
        fields = ['name', 'nin', 'contact', 'photo']

class FaceRegistrationForm(forms.ModelForm):
    class Meta:
        model = FaceRegistration
        fields = ['student', 'pickup_person', 'face_data']

class PickupScheduleForm(forms.ModelForm):
    class Meta:
        model = PickupSchedule
        fields = ['student', 'pickup_person', 'pickup_time']        