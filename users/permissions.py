from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()

class CanViewAndEditOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.method in ['PUT', 'PATCH', 'GET']
