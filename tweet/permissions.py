from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):   #New permission

    def has_permission(self, request, view):
        return True

    def has_object_permission(self,request,view,obj):

        if request.method in permissions.SAFE_METHODS: #if request method is GET, HEAD or OPTIONS, allow, since anyone can read it

            return True

        return request.user == obj.owner               #if you want to CREATE, DELETE or UPDATE, you must be the object owner
