from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        #Si se trata de un administrador permitirá todo
        if request.user.is_superuser:
            return True
        #Si no se trata de un administrador ahora dará permisos especiales 
        if request.method in ['GET', 'HEAD', 'OPTIONS','POST']:
            return request.user.is_authenticated
        else:
            return obj.user == request.user
        
