from rest_framework import permissions


class IsUserOrModeratorOrReadOnly(permissions.BasePermission):
    
    
    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            
            return True
            
        return request.user == obj or request.user.is_staff
        

class IsModerator(permissions.BasePermission):
    
    
    def has_object_permission(self, request, view, obj):
        
        
        return request.user.is_staff