from django.db import models
from django.utils import timezone
#from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class LecturerUserManager(BaseUserManager):
    def create_user(self, staff_id, full_name, department, password=None):
        if not staff_id:
            raise ValueError("Staff ID is required")
        user = self.model(staff_id=staff_id, full_name=full_name, department=department)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, staff_id, full_name, department, password=None):
        user = self.create_user(staff_id, full_name, department, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
#from .managers import LecturerUserManager  # Make sure you import your manager

class LecturerUser(AbstractBaseUser, PermissionsMixin):
    staff_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'staff_id'
    REQUIRED_FIELDS = ['full_name', 'department']

    objects = LecturerUserManager()

    def __str__(self):
        return self.full_name

    @property
    def username(self):
        # Return staff_id as a stand-in for 'username'
        return self.staff_id

# If this is inside models.py
from django.db import models
#from .lecturer import LecturerUser  # Adjust if LecturerUser is in another app
# attendance/models.py
from django.db import models
#from users.models import LecturerUser  # Adjust this import based on your project

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    lecturer = models.ForeignKey(LecturerUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        # DO NOT add abstract = True







class Student(models.Model):
    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def full_name(self):
        return self.student_name

    def __str__(self):
        return f"{self.student_name} ({self.student_id})"






class HOD(models.Model):
    user = models.OneToOneField(LecturerUser, on_delete=models.CASCADE)
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return f"HOD - {self.department_name}"


# models.py
from django.db import models
#from .course import Course  # or wherever Course is defined

class AttendanceRecord(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    student_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.course.code}"


class AttendanceWindow(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    location_lat = models.FloatField()
    location_lon = models.FloatField()
    distance_limit = models.FloatField(default=0.0, help_text="Distance in meters")


    def __str__(self):
        return f"Window for {self.course.code}"


class AttendanceSession(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    is_open = models.BooleanField(default=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    allowed_distance = models.IntegerField(help_text="Distance in meters")

    def __str__(self):
        return f"{self.course.code} - {self.start_time.date()}"



class Attendance(models.Model):
    student_id = models.CharField(max_length=100, null=True, blank=True)
    student_name = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    student_latitude = models.FloatField(null=True, blank=True)
    student_longitude = models.FloatField(null=True, blank=True)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student_name} - {self.timestamp.date()}"




# Course
# attendance/models.py
# attendance/models.py

#from django.db import models
#from .models import LecturerUser  # ensure this import works
#from django.db import models
#from .lecturer import LecturerUser  # Or wherever LecturerUser is defined

#class Course(models.Model):
    #name = models.CharField(max_length=100)
    #code = models.CharField(max_length=20, unique=True)
    #lecturer = models.ForeignKey(LecturerUser, on_delete=models.CASCADE)

    #def __str__(self):
        #return f"{self.name} ({self.code})"




# AttendanceSession
#class AttendanceSession(models.Model):
    #course = models.ForeignKey(Course, on_delete=models.CASCADE)
    #lecturer = models.ForeignKey(LecturerUser, on_delete=models.CASCADE)
    #created_at = models.DateTimeField(auto_now_add=True)
    #end_time = models.DateTimeField()
    #max_distance = models.FloatField(help_text="Enter distance in meters")

