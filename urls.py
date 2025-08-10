# --- urls.py ---
from django.urls import path
from . import views
from django.urls import path
from attendance import views
#from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.student_register, name='student_register'),
    #path('mark/<int:course_id>/', views.mark_attendance, name='mark_attendance'),
    path('dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('toggle/<int:course_id>/', views.toggle_attendance, name='toggle_attendance'),
    path('export/<int:course_id>/', views.export_attendance_pdf, name='export_attendance_pdf'),
    path('hod/', views.hod_dashboard, name='hod_dashboard'),
    #path('signup/', views.signup, name='signup'),
     #path('register/success/', views.registration_success, name='registration_success'),



    # ✅ FIXED: use auth_views directly (not from views)
    #path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
       #path('attendance/mark/<int:course_id>/', views.mark_attendance, name='mark_attendance'),
    
      #path('login/', views.student_login, name='student_login'),
      path('student/login/', views.student_login_view, name='student_login'),
    #path('mark-attendance/<str:student_id>/', views.mark_attendance, name='mark_attendance'),

    #path('enter-course/<str:student_id>/', views.enter_course_code, name='enter_course_code'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('mark-attendance/<str:student_id>/<str:course_code>/', views.mark_attendance, name='mark_attendance'),
    
    #path('download-pdf/', views.download_attendance_pdf, name='download_attendance_pdf'),
    path('set-attendance-window/', views.set_attendance_window, name='set_attendance_window'),
    # urls.py
    #path('export-attendance/<str:course_code>/<str:date_str>/', views.generate_attendance_pdf, name='export_attendance_pdf'),
    path('success/', views.registration_success, name='registration_success'),
      #path('student/attendance/', views.enter_course_code_view, name='enter_course_code'),
      path('student/enter-course/', views.enter_course_code_view, name='enter_course_code'),

       #path('lecturer/register/', views.lecturer_register, name='lecturer_register'),
    #path('lecturer/login/', views.lecturer_login, name='lecturer_login'),
     path('lecturer/add-course/', views.add_course, name='add_course'),
       path('open-session/', views.open_session, name='open_session'),
      #path('lecturer/register/', views.lecturer_register, name='lecturer_register'),
      #path('lecturer/register/', views.lecturer_register, name='lecturer_register'),
       #path('lecturer/register/', views.lecturer_register, name='lecturer_register'),

    path('register/success/', views.registration_success, name='registration_success'),
    path('login/', views.lecturer_register, name='lecturer_register'),
      

    path('lecturer/login/', views.lecturer_login, name='lecturer_login'),
    path('lecturer/register/', views.lecturer_register, name='lecturer_register'),
    #path('lecturer/dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),




    #path('lecturer/dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),
    path('lecturer/add-course/', views.add_course, name='add_course'),
   # path('lecturer/open-attendance/', views.open_attendance, name='open_attendance'),
    path('lecturer/download-pdf/<int:session_id>/', views.export_attendance_pdf, name='download_attendance_pdf'),

    path('lecturer/dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),

  ]