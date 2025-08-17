from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'First_name', 'Last_name', 'role', 'phone', 'profile_photo', 'gender', 'date_joined')
    list_filter = ('role', 'gender', 'date_joined')
    search_fields = ('username', 'email', 'phone')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('user_id','name', 'email', 'subject', 'message', 'created_at', 'is_read')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'mobile', 'message', 'created_at', 'is_read')
    search_fields = ('name', 'email', 'mobile')
    list_filter = ('created_at',)

@admin.register(IRSensor)
class IRSensorAdmin(admin.ModelAdmin):
    list_display = ('value', 'timestamp')
    list_filter = ('value', 'timestamp')
    ordering = ('-timestamp',)

@admin.register(WaterLevelSensor)
class WaterLevelSensorAdmin(admin.ModelAdmin):
    list_display = ('level', 'timestamp')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(SmokeSensor)
class SmokeSensorAdmin(admin.ModelAdmin):
    list_display = ('ppm', 'timestamp')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(SoilMoistureSensor)
class SoilMoistureSensorAdmin(admin.ModelAdmin):
    list_display = ('moisture_percent', 'timestamp')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(FireLevelSensor)
class FireLevelSensorAdmin(admin.ModelAdmin):
    list_display = ('level', 'timestamp')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)