from rest_framework import permissions
from app.models import *
import redis
from django.conf import settings
session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import PermissionDenied

class IsManager(permissions.BasePermission): 
    def has_permission(self, request, view): 
        # access_token = request.headers.get('Authorization') 
        access_token = request.COOKIES["session_id"]
 
        if access_token is None: 
            return False 
 
        try: 
            username = session_storage.get(access_token).decode('utf-8') 
        except Exception as e: 
            return False 
        user = CustomUser.objects.filter(email=username).first() 
        return user.is_superuser 
     

class IsAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.COOKIES)
        access_token = request.COOKIES.get("session_id")
        print('cheeeeck', access_token)

        if access_token is None:
            raise PermissionDenied("Permission Denied")

        try:
            user = session_storage.get(access_token).decode('utf-8')
        except Exception as e:
            return False

        return True