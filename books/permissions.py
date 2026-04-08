from rest_framework.permissions import BasePermission
from users.models import Author

class is_Author(BasePermission):
    
    def has_permission(self, request, view ):
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return Author.objects.filter(user=request.user).exists()
        return True