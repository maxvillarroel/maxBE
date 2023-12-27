from rest_framework.permissions import BasePermission
class IsSelf(BasePermission):
    message = 'Editing another account not allowed.'
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
    
class SafeFieldsOnly(BasePermission):
    message = 'Priviledge escalation not allowed.'
    def has_permission(self, request, view):
        if 'is_staff' in request.data:
            if  request.data['is_staff'] == 'True' and not request.user.is_staff:
                return False
        if 'is_superuser' in request.data:
            if  request.data['is_superuser'] == 'True' and not request.user.is_superuser:
                return False
        return True