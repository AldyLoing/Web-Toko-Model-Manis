from django.contrib.auth.models import User

class AutoStaffMiddleware:
    """
    Middleware untuk otomatis memberikan hak staff kepada user yang login
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Cek jika user sudah login dan belum menjadi staff
        if request.user.is_authenticated and not request.user.is_staff:
            # Set user sebagai staff dan superuser
            request.user.is_staff = True
            request.user.is_superuser = True
            request.user.save()

        response = self.get_response(request)
        return response