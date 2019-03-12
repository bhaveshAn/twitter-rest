from django.shortcuts import render

# Create your views here.
from user.models import CustomUser

from user.serializers import UserSerializerCreate, UserSerializerOut

from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserList(generics.ListAPIView): #Generic class based view to list users
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerOut

class UserDetail(generics.RetrieveAPIView): #Generic class based view to show specific user
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerOut
    lookup_field = 'username'               #Field can be looked up with using the username


class UserCreate(APIView): #Class to create user

    def post(self, request, format=None):
        serializer = UserSerializerCreate(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFollow(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def getUser(self,username):      #Fetch user from database

        try:
            user = CustomUser.objects.get(username = username)
        except CustomUser.DoesNotExist:
            raise Http404

        return user   #Return associated user

    def put(self,request,username,format=None):

        user = self.getUser(username)
        user.profile.follow(self.request.user)
        return Response(status=status.HTTP_201_CREATED)
