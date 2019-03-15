from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User

from tweet.models import Tweet, Reply
from tweet.serializers import (
    TweetReadSerializer,
    TweetMakeSerializer,
    ReplyTweetSerializerCreate,
)
from tweet.permissions import IsOwnerOrReadOnly

from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TweetList(generics.ListAPIView):  # Generic class based view to list users
    queryset = Tweet.objects.all()
    serializer_class = TweetReadSerializer


class TweetDetail(
    generics.RetrieveAPIView
):  # Generic class based view to show specific user
    queryset = Tweet.objects.all()
    serializer_class = TweetMakeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class TweetPost(generics.CreateAPIView):  # Generic class based view to create tweets

    queryset = Tweet.objects.all()
    serializer_class = TweetMakeSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )  # If user is not the owner, each tweet is read only

    def perform_create(self, serializer):  # When creating tweet
        serializer.save(
            owner=self.request.user
        )  # Owner of tweet is set as the user that sent the request


class UserTweets(APIView):  # View to get tweets from specific user

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, username, format=None):

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            raise Http404

        tweets = user.tweets.all()
        serialized = TweetReadSerializer(tweets, many=True)

        return Response(serialized.data)


class UserTweetsDetail(APIView):  # View to get specific tweet from specific user
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )  # If user is not the owner, each tweet is read only

    def getTweet(self, username, pk):  # Fetch tweet from database

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

        try:
            tweet = user.tweets.get(id=pk)
        except Tweet.DoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, user.tweets.get(id=pk))
        return user.tweets.get(id=pk)  # Return tweet with associated id

    def get(self, request, username, pk, format=None):  # GET tweet

        tweet = self.getTweet(username, pk)
        serialized = TweetReadSerializer(tweet)

        return Response(serialized.data)

    def delete(self, request, username, pk, format=None):  # Delete tweet
        tweet = self.getTweet(username, pk)
        tweet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeTweet(APIView):  # PUT to like specific tweet

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def put(self, request, pk, format=None):

        tweet = Tweet.objects.get(id=pk)
        tweet.likeTweet(self.request.user)  # Call countlikes function
        return Response(status=status.HTTP_201_CREATED)


class ReplyTweetPost(APIView):  # Class to create Replies
    def post(self, request, pk, format=None):
        serializer = ReplyTweetSerializerCreate(data=request.data)
        if serializer.is_valid():
            tweet = Tweet.objects.get(id=pk)
            serializer.save(owner=self.request.user, tweet=tweet)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
