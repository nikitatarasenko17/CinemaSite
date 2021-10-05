from rest_framework.permissions import BasePermission
from cinema.models import Hall, Movies, Sessions, Purchase, MyUser  

class SuperUserPermissionToSessionUpdate(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT']:
            sessions = Purchase.objects.filter(purchase_session__is_active=True, quantity__gte=0)
            if sessions:
                return False
        return True

    def has_permission(self, request, view):
        return True


