from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.IntegerField()
    First_name = models.CharField(max_length=100)
    Last_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=[
        ('user', 'USER'),
        ('admin', 'ADMIN'),
    ])
    phone = models.BigIntegerField(null=True, blank=True)
    profile = models.ImageField(upload_to='profile')  # Fixed typo here
    gender = models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def profile_photo(self):
        if self.profile:
            return mark_safe('<img src="{}" width="100px">'.format(self.profile.url))
        return "No Image"


class ContactMessage(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # NEW FIELD

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class Complaint(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # NEW FIELD
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Complaint from {self.name}"


class IRSensor(models.Model):
    value = models.IntegerField()  # True for detected, False otherwise
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"IRSensor - {'Detected' if self.value else 'Not Detected'} at {self.timestamp}"

class WaterLevelSensor(models.Model):
    level = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Water Level - {self.level} at {self.timestamp}"

class SmokeSensor(models.Model):
    ppm = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Smoke - {self.ppm} ppm at {self.timestamp}"

class SoilMoistureSensor(models.Model):
    moisture_percent = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Soil Moisture - {self.moisture_percent}% at {self.timestamp}"

class FireLevelSensor(models.Model):
    level = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fire Level - {self.level} at {self.timestamp}"