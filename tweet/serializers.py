from tweet.models import Tweet, Reply
from rest_framework import serializers

class TweetReadSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source = 'owner.username')        #Make these fields read only
    likes = serializers.IntegerField(source = 'appreciators.count')
    replies = serializers.IntegerField(source = 'replies.count')
    class Meta:
        model = Tweet
        fields = ('id', 'created', 'text', 'owner', 'likes','appreciators', 'replies')

class TweetMakeSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source = 'owner.username')        #Make these fields read only
    class Meta:
        model = Tweet
        fields = ('id','text','owner')


class ReplyTweetSerializerCreate(serializers.ModelSerializer):    #Serializer for creating an account

    text = serializers.CharField()
    owner = serializers.ReadOnlyField(source = 'owner.username')

    class Meta:
        model = Reply
        fields = ('owner','text', 'tweet', 'created')
