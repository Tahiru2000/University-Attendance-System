from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, LecturerUser, Course, Attendance, HOD, AttendanceRecord

# Register Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'student_id', 'registered_at')
    search_fields = ('student_name', 'student_id')


# Register LecturerUser (only once)
@admin.register(LecturerUser)
class LecturerUserAdmin(UserAdmin):
    model = LecturerUser
    list_display = ('staff_id', 'full_name', 'department', 'is_staff', 'is_superuser')
    ordering = ('staff_id',)
    search_fields = ('staff_id', 'full_name')
    fieldsets = (
        (None, {'fields': ('staff_id', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('staff_id', 'full_name', 'department', 'password1', 'password2'),
        }),
    )


# Register Course
#@admin.register(Course)
#class CourseAdmin(admin.ModelAdmin):
    #list_display = ['code', 'name', 'lecturer']
    #list_filter = ['lecturer']


# Register Attendance
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student_name', 'student_id', 'timestamp', 'student_latitude', 'student_longitude', 'is_valid']
    list_filter = ['is_valid', 'timestamp']


# Register HOD
@admin.register(HOD)
class HODAdmin(admin.ModelAdmin):
    list_display = ('user', 'department_name')
    search_fields = ('department_name', 'user__staff_id')


# Optional: Register AttendanceRecord if needed
#@admin.register(AttendanceRecord)
#class AttendanceRecordAdmin(admin.ModelAdmin):
   # list_display = ['student', 'course', 'timestamp']  # ✅ Correct field name
    #list_filter = ['course', 'timestamp']              # ✅ Must match model


from django.contrib import admin
from .models import AttendanceRecord, AttendanceSession, AttendanceWindow, Course

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'student_name', 'course', 'timestamp']
    list_filter = ['course', 'timestamp']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'lecturer']
    list_filter = ['lecturer']
