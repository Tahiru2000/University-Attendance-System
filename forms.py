# --- forms.py ---

from django import forms
from .models import (
    Student, Attendance, AttendanceWindow,
    AttendanceSession, Course, LecturerUser
)


# ----------------------------
# Student Forms
# ----------------------------

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'student_id']


class StudentLoginForm(forms.Form):
    student_id = forms.CharField(label="Student ID", max_length=20)


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = [
            'student_id',
            'student_name',
            'student_latitude',
            'student_longitude',
            'is_valid',
        ]


# ----------------------------
# Lecturer Forms
# ----------------------------

class LecturerRegistrationForm(forms.ModelForm):
    class Meta:
        model = LecturerUser
        fields = ['full_name', 'staff_id', 'department']

    def clean_staff_id(self):
        staff_id = self.cleaned_data.get('staff_id')
        if LecturerUser.objects.filter(staff_id=staff_id).exists():
            raise forms.ValidationError("A user with this Staff ID already exists.")
        return staff_id

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(LecturerUser.objects.make_random_password())  # Set random password
        if commit:
            user.save()
        return user


#class StaffIDLoginForm(forms.Form):
    #staff_id = forms.CharField(label="Staff ID", max_length=50)

#from django import forms

class LecturerLoginForm(forms.Form):
    staff_id = forms.CharField(label="Staff ID", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



# ----------------------------
# Course & Attendance Forms
# ----------------------------

#class CourseForm(forms.ModelForm):
    #class Meta:
        #model = Course
        #fields = ['name', 'code']

#class AttendanceWindowForm(forms.ModelForm):
    #class Meta:
        #model = AttendanceWindow
        #fields = ['course', 'end_time', 'distance_limit']  # ✅ Only valid model fields

from django import forms
from .models import AttendanceWindow, Course

class AttendanceWindowForm(forms.ModelForm):
    class Meta:
        model = AttendanceWindow
        fields = ['course', 'end_time', 'location_lat', 'location_lon', 'distance_limit']

    def __init__(self, *args, **kwargs):
        lecturer = kwargs.pop('lecturer', None)
        super().__init__(*args, **kwargs)
        if lecturer:
            self.fields['course'].queryset = Course.objects.filter(lecturer=lecturer)

#class AttendanceSessionForm(forms.ModelForm):
    #class Meta:
        #model = AttendanceSession
        #fields = ['course', 'end_time', 'latitude', 'longitude', 'allowed_distance']



from django import forms
from .models import Course, AttendanceSession

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']

    def __init__(self, *args, **kwargs):
        self.lecturer = kwargs.pop('lecturer', None)
        super().__init__(*args, **kwargs)

class AttendanceSessionForm(forms.ModelForm):
    class Meta:
        model = AttendanceSession
        fields = ['course', 'end_time', 'allowed_distance']

