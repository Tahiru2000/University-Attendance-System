# backend.py
from django.contrib.auth.backends import BaseBackend
from .models import LecturerUser

class StaffIDBackend(BaseBackend):
    def authenticate(self, request, staff_id=None):
        try:
            user = LecturerUser.objects.get(staff_id=staff_id)
            return user
        except LecturerUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return LecturerUser.objects.get(pk=user_id)
        except LecturerUser.DoesNotExist:
            return None
