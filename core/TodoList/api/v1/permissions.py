from rest_framework import permissions # type: ignore
from rest_framework.response import Response # type: ignore



class IsOwnerPermissions(permissions.BasePermission):
    def has_object_permission(self , request , view , obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        

        return obj.user == request.user