# attendance/tasks.py
from django_q.tasks import schedule
from django.utils.timezone import now
from .models import AttendanceSession

def close_expired_sessions():
    sessions = AttendanceSession.objects.filter(is_open=True, end_time__lte=now())
    for session in sessions:
        session.is_open = False
        session.save()
    return f"Closed {sessions.count()} session(s)"

