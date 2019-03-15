# Create your views here.
from rest_framework import generics
from rest_framework import permissions

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user.models import CustomUser
from user.serializers import UserSerializerCreate, UserSerializerOut


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerOut


class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializerOut
    lookup_field = "username"


class UserCreate(APIView):
    def post(self, request, format=None):
        serializer = UserSerializerCreate(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFollow(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def getUser(self, username):

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise Http404

        return user

    def put(self, request, username, format=None):

        user = self.getUser(username)
        user.profile.follow(self.request.user)
        return Response(status=status.HTTP_201_CREATED)
