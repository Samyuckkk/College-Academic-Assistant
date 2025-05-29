from django.db import models
from django.contrib.auth.models import User
# Create your models here.
    
class Appointment(models.Model):
    student_name = models.CharField(max_length=255)
    student_username = models.CharField(max_length=255)
    message = models.TextField()
    teacher_name = models.CharField(max_length=255)
    teacher_username = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment with {self.teacher_name} by {self.student_name}"
    

class AcceptedAppointment(models.Model):
    student_name = models.CharField(max_length=255)
    student_username = models.CharField(max_length=255)
    teacher_name = models.CharField(max_length=255)
    teacher_username = models.CharField(max_length=255)
    message = models.TextField()
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    accepted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} with {self.teacher_name} on {self.appointment_date} at {self.appointment_time}"
    


class Subject(models.Model):
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)
    course_type = models.CharField(max_length=100, default="Compulsary")
    category = models.CharField(max_length=50)
    credits = models.IntegerField()
    lecture_hours = models.IntegerField()
    pr_hours = models.IntegerField()
    semester = models.IntegerField()


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course_code'], name='unique_course_code'),
            models.UniqueConstraint(fields=['course_name'], name='unique_course_name'),
        ]


    def __str__(self):
        return f"{self.course_code} - Semester {self.semester}"    
    
    