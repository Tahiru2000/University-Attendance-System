from django.shortcuts import render

# Create your views here.
#from .models import Student, LecturerUser, Course, Attendance, HOD

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Student, Attendance, HOD
from .forms import  AttendanceForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date
from django.contrib.auth.models import Group
import math
from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import now
from .models import Course, Attendance, Student
from django.http import HttpResponseForbidden
from .forms import StudentRegistrationForm
from .forms import StudentLoginForm
from .models import Student, Course, AttendanceRecord
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.utils import timezone
from .models import Course, AttendanceWindow
from .forms import AttendanceWindowForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AttendanceSession, Attendance
from geopy.distance import geodesic
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import StudentRegistrationForm

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('registration_success')
            except Exception as e:
                print(f"Save error: {e}")
    else:
        form = StudentRegistrationForm()  # For GET requests, show empty form

    return render(request, 'student_register.html', {'form': form})







# Make sure Student is imported



from .models import AttendanceRecord
# Helper function to check distance in meters
def is_within_distance(session_lat, session_lon, student_lat, student_lon, allowed_distance):
    session_location = (session_lat, session_lon)
    student_location = (student_lat, student_lon)
    return geodesic(session_location, student_location).meters <= allowed_distance

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_code = request.POST.get('course_code')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Validate inputs
        if not all([student_id, course_code, latitude, longitude]):
            messages.error(request, "All fields are required.")
            return redirect('mark_attendance')

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except ValueError:
            messages.error(request, "Invalid latitude or longitude.")
            return redirect('mark_attendance')

        # Find open session for the course
        session = AttendanceSession.objects.filter(course__course_code=course_code, is_open=True).last()

        if session:
            if is_within_distance(session.latitude, session.longitude, latitude, longitude, session.allowed_distance):
                # Optional: Prevent double attendance by the same student
                already_marked = Attendance.objects.filter(session=session, student_id=student_id).exists()
                if already_marked:
                    messages.warning(request, "You have already marked attendance for this session.")
                else:
                    Attendance.objects.create(
                        session=session,
                        student_id=student_id,
                        student_name=request.user.get_full_name(),  # or input from form
                        student_latitude=latitude,
                        student_longitude=longitude,
                        is_valid=True
                    )
                    messages.success(request, "Attendance marked successfully.")
            else:
                messages.error(request, "You are too far from the lecture location to mark attendance.")
        else:
            messages.error(request, "No active attendance session found for this course.")

        return redirect('mark_attendance')  # Change to appropriate template/view name

    return render(request, 'student/mark_attendance.html') 



    

#def mark_attendance(request, student_id, course_code):
    #return render(request, 'attendance/mark_attendance.html', {
        #'student_id': student_id,
        #'course_code': course_code
    #})


# attendance/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CourseForm, AttendanceWindowForm
from .models import Course, AttendanceWindow, Attendance
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Course, AttendanceWindow
from .forms import CourseForm, AttendanceWindowForm

@login_required
def lecturer_dashboard(request):
    lecturer = request.user
    courses = Course.objects.filter(lecturer=lecturer)
    course_form = CourseForm()
    attendance_form = AttendanceWindowForm(lecturer=lecturer)  # <-- pass lecturer here

    if request.method == 'POST':
        if 'add_course' in request.POST:
            course_form = CourseForm(request.POST)
            if course_form.is_valid():
                course = course_form.save(commit=False)
                course.lecturer = lecturer
                course.save()
                messages.success(request, "Course added successfully.")
                return redirect('lecturer_dashboard')

        elif 'open_attendance' in request.POST:
            attendance_form = AttendanceWindowForm(request.POST, lecturer=lecturer)  # <-- and here
            if attendance_form.is_valid():
                attendance_window = attendance_form.save(commit=False)
                attendance_window.start_time = timezone.now()
                attendance_window.save()
                messages.success(request, "Attendance session opened.")
                return redirect('lecturer_dashboard')

    attendance_sessions = AttendanceWindow.objects.filter(course__lecturer=lecturer)

    return render(request, 'attendance/lecturer_dashboard.html', {
        'course_form': course_form,
        'attendance_form': attendance_form,
        'courses': courses,
        'attendance_sessions': attendance_sessions
    })










@login_required
def toggle_attendance(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.is_open = not course.is_open
    course.save()
    return redirect('lecturer_dashboard')


from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from .models import Attendance, Course

def export_attendance_pdf(request, session_id):
    # Check if the user is authenticated and a lecturer
    if not request.user.is_authenticated or not hasattr(request.user, 'staff_id'):
        return HttpResponse("Unauthorized", status=401)

    # Filter attendance data by session ID (e.g., course or session)
    try:
        course = Course.objects.get(id=session_id, lecturer=request.user)
    except Course.DoesNotExist:
        return HttpResponse("Course not found", status=404)

    attendance_records = Attendance.objects.filter(course=course)

    # Create the HTTP response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{course.code}_attendance.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"Attendance Sheet for {course.name} ({course.code})", styles['Title']))
    elements.append(Spacer(1, 12))

    data = [['Student Name', 'Student ID', 'Timestamp', 'Valid']]

    for record in attendance_records:
        data.append([
            record.student_name,
            record.student_id,
            record.timestamp.strftime("%Y-%m-%d %H:%M"),
            "Yes" if record.is_valid else "No"
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ]))

    elements.append(table)
    doc.build(elements)

    return response



@login_required
def hod_dashboard(request):
    if not hasattr(request.user, 'hod'):
        return HttpResponse("Unauthorized access.")
    all_courses = Course.objects.all()
    return render(request, 'attendance/hod_dashboard.html', {'courses': all_courses})



def is_within_radius(lat1, lng1, lat2, lng2, radius_meters=50):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    a = math.sin(delta_phi/2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance <= radius_meters

# views.py
#@login_required
def home(request):
    student_id = request.user.username  # or however you track student ID
    courses = Course.objects.all()      # assuming you have a Course model
    return render(request, 'home.html', {
        'student_id': student_id,
        'courses': courses
    })



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})




# views.py
def registration_success(request):
    return render(request, 'registration_success.html')




#def student_login_view(request):
    #if request.method == 'POST':
        #student_id = request.POST['student_id']
        #password = request.POST['password']
        #user = authenticate(request, username=student_id)
        #if user is not None:
            #login(request, user)
            #return redirect()
        #else:
            #return render(request, 'student_login.html', {'error': 'Invalid credentials'})
    #return render(request, 'attendance/student_login.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Student

def student_login_view(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = Student.objects.get(student_id=student_id)
            request.session['student_id'] = student.id  # Store session
            return redirect('enter_course_code')  # ✅ Redirect here
        except Student.DoesNotExist:
            messages.error(request, "Invalid Student ID")
    return render(request, 'attendance/student_login.html')
 # ✅ correct path

    


#from django.shortcuts import render, redirect
#from .models import Student

#def student_login(request):
    #if request.method == 'POST':
        #student_id = request.POST.get('student_id')
        #student = Student.objects.filter(student_id=student_id).first()
        #if student:
            #request.session['student_id'] = student_id
            #return redirect('enter_course_code')  # You define this next
        #else:
            #return render(request, 'student_login.html', {'error': 'Invalid Student ID'})
    #return render(request, 'student_login.html')





#@login_required
#def enter_course_code(request, student_id):
    #if request.method == 'POST':
        #course_code = request.POST.get('course_code').strip().upper()
        #try:
            #course = Course.objects.get(code=course_code)
            #return redirect('mark_attendance', course_code=course.code)
        #except Course.DoesNotExist:
            #messages.error(request, 'Invalid course code. Please try again.')
    #return render(request, 'enter_course_code.html',{'student_id': student_id})



# attendance/views.py (continued - course code, session, and attendance logic)
import math
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import AttendanceSession, AttendanceRecord, Student


# Helper function to compute distance in meters between two lat/lon points
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Distance in meters


def enter_course_code_view(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('student_login')

    if request.method == 'POST':
        course_code = request.POST.get('course_code')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        try:
            session = AttendanceSession.objects.get(
                course__code=course_code,
                is_open=True,
                end_time__gte=timezone.now()
            )
        except AttendanceSession.DoesNotExist:
            messages.error(request, "No open attendance session for this course.")
            return redirect('enter_course_code')

        try:
            lat1 = float(latitude)
            lon1 = float(longitude)
            lat2 = float(session.latitude)
            lon2 = float(session.longitude)

            distance = haversine_distance(lat1, lon1, lat2, lon2)

            if distance > session.allowed_distance:
                messages.error(request, f"You are too far from the attendance location. Distance: {int(distance)}m")
                return redirect('enter_course_code')

            # Mark attendance
            student = Student.objects.get(id=student_id)
            AttendanceRecord.objects.get_or_create(
                student=student,
                session=session,
                defaults={
                    'timestamp': timezone.now(),
                    'latitude': lat1,
                    'longitude': lon1
                }
            )
            messages.success(request, "Attendance recorded successfully.")
            return redirect('attendance_success')

        except Exception as e:
            messages.error(request, "Error during attendance marking: " + str(e))
            return redirect('enter_course_code')

    return render(request, 'attendance/enter_course_code.html')







#def generate_attendance_pdf(request, course_code, date_str):
    #if not request.user.is_staff and not request.user.groups.filter(name='Lecturers').exists():
        #return HttpResponse("Unauthorized", status=403)

    #course = Course.objects.get(code=course_code)
    #date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    #records = AttendanceRecord.objects.filter(course=course, date=date_obj).select_related('student')

    #template = get_template('attendance_pdf.html')
    #html = template.render({'course': course, 'records': records, 'date': date_obj})

    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = f'attachment; filename="{course.code}_{date_str}_attendance.pdf"'
    #pisa_status = pisa.CreatePDF(html, dest=response)

    #if pisa_status.err:
        #return HttpResponse('PDF generation error', status=500)

    #return response



@login_required
def set_attendance_window(request):
    if not request.user.groups.filter(name='Lecturers').exists():
        return render(request, 'not_authorized.html')
    form.fields['course'].queryset = Course.objects.filter(lecturer=request.user)
    if request.method == 'POST':
        form = AttendanceWindowForm(request.POST)
        if form.is_valid():
            attendance_window = form.save(commit=False)
            attendance_window.save()
            return redirect('view_windows')  # Redirect to a list of set windows
    else:
        form = AttendanceWindowForm()

    return render(request, 'set_attendance_window.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Course, LecturerUser

def add_course(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        course_code = request.POST.get('course_code')
        lecturer_id = request.session.get('lecturer_id')

        if course_name and course_code and lecturer_id:
            lecturer = LecturerUser.objects.get(id=lecturer_id)
            Course.objects.create(name=course_name, code=course_code, lecturer=lecturer)
            messages.success(request, "Course added successfully.")
            return redirect('lecturer_dashboard')
        else:
            messages.error(request, "Please provide all required fields.")

    return render(request, 'add_course.html')






# views.py
# views.py
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Course, AttendanceSession, LecturerUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
@login_required
def open_session(request):
    # ✅ Get the Lecturer object linked to the logged-in user
    try:
        lecturer = LecturerUser.objects.get(user=request.user)
    except LecturerUser.DoesNotExist:
        return HttpResponse("Lecturer profile not found", status=404)

    # ✅ Now it's safe to filter using the Lecturer instance
    courses = Course.objects.filter(lecturer=lecturer)

    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        end_time_str = request.POST.get('end_time')

        try:
            course = Course.objects.get(id=course_id, lecturer=lecturer)
        except Course.DoesNotExist:
            return HttpResponse("Course not found or access denied", status=404)

        now = timezone.now()

        try:
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
            end_datetime = timezone.make_aware(datetime.combine(now.date(), end_time))
        except ValueError:
            return HttpResponse("Invalid time format", status=400)

        AttendanceSession.objects.create(
            course=course,
            lecturer=lecturer,
            start_time=now,
            end_time=end_datetime
        )

        return redirect('lecturer_dashboard')

    return render(request, 'open_session.html', {'courses': courses})





from geopy.distance import geodesic

def is_within_distance(lat1, lon1, lat2, lon2, max_dist):
    return geodesic((lat1, lon1), (lat2, lon2)).meters <= max_dist



# views.py
from django.shortcuts import render, redirect
from .forms import LecturerRegistrationForm

def lecturer_register(request):
    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lecturer_login')

    else:
        form = LecturerRegistrationForm()
    return render(request, 'lecturer_register.html', {'form': form})

def registration_success(request):
    return render(request, 'registration_success.html')




from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LecturerLoginForm
from django.contrib import messages
from django.http import HttpResponseRedirect

def lecturer_login(request):
    if request.method == 'POST':
        form = LecturerLoginForm(request.POST)
        if form.is_valid():
            staff_id = form.cleaned_data['staff_id']
            #password = form.cleaned_data['password']
            user = authenticate(request, staff_id=staff_id,)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/lecturer/dashboard/') # Make sure this URL name exists
            else:
                messages.error(request, 'Invalid staff ID or password.')
    else:
        form = LecturerLoginForm()
    return render(request, 'lecturer_login.html', {'form': form})
