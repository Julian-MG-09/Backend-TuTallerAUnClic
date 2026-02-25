from rest_framework.permissions import BasePermission





class EsCliente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol.nombre == "CLIENTE"
    
    
class EsEmpresa(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol.nombre == "EMPRESA"
    
    
class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol.nombre == "ADMIN"
