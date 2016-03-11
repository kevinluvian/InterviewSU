from rest_framework import permissions

class IsIntervieweeHimself(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # komentarin 2 baris ini buat edit profile user
        # if request.method in permissions.SAFE_METHODS:
        #   return True
        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user

class IsInterviewer(permissions.BasePermission):
    """
    Custom permission to check whether this particular user is interviewer
    """
    def has_object_permission(self, request, view, obj):
        return not obj.user.interviewer.all()


class IsAnonymous(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user
    def has_permission(self, request, view):
        return request.method != 'POST' or not(request.user and request.user.is_authenticated())

