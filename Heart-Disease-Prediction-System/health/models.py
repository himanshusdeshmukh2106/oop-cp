from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from .choices import DOCTOR_STATUS

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username

class Doctor(models.Model):
    status = models.IntegerField(DOCTOR_STATUS, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    doj = models.DateField(null=True)
    dob = models.DateField(null=True)
    image = models.FileField(null=True)
    
    # Location fields for map integration
    hospital_name = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    specialization = models.CharField(max_length=200, null=True, blank=True, default='Cardiologist')

    def __str__(self):
        return self.user.username

class Admin_Helath_CSV(models.Model):
    name = models.CharField(max_length=100, null=True)
    csv_file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name

class Search_Data(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    prediction_accuracy = models.CharField(max_length=100,null=True,blank=True)
    result = models.CharField(max_length=100,null=True,blank=True)
    values_list = models.CharField(max_length=100,null=True,blank=True)
    created = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.patient.user.username

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    messages = models.TextField(null=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.user.username


class ECG_Prediction(models.Model):
    """Store ECG image predictions"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    ecg_image = models.ImageField(upload_to='ecg_images/', null=True)
    prediction_code = models.IntegerField(null=True)  # 0=Abnormal, 1=MI, 2=Normal, 3=History of MI
    prediction_label = models.CharField(max_length=100, null=True)
    prediction_message = models.TextField(null=True)
    confidence = models.FloatField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.patient.user.username} - {self.prediction_label}"
    
    class Meta:
        ordering = ['-created']


class Appointment(models.Model):
    """Store appointment bookings"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # Link to prediction if appointment is made after prediction
    related_prediction = models.ForeignKey(Search_Data, on_delete=models.SET_NULL, null=True, blank=True)
    related_ecg = models.ForeignKey(ECG_Prediction, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.patient.user.username} - Dr. {self.doctor.user.last_name} on {self.appointment_date}"
    
    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
