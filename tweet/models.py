from django.db import models

# Create your models here.

from user.models import CustomUser


class Tweet(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )  # Field showing when tweet was created
    text = models.CharField(max_length=140)  # Text content of tweet, max char count 140
    owner = models.ForeignKey(
        CustomUser, related_name="tweets", on_delete=models.CASCADE
    )  # Each tweet is associated with a user
    appreciators = models.ManyToManyField(
        CustomUser, related_name="appreciated", blank=True
    )

    class Meta:
        ordering = ("created",)  # Tweets are ordered in date created

    def __str__(self):
        return self.text  # When outputting in console, show text field of tweet

    def likeTweet(self, user):
        if self.appreciators.filter(
            id=user.id
        ).exists():  # If user already liked tweet, unlike it, otherwise like it
            self.appreciators.remove(user)
        else:
            self.appreciators.add(user)

        self.save()

    def countLikes(self):
        self.likes = self.appreciators.count()

    def replyTweet(self, reply):
        self.replies.add(reply)

        self.save()

    def countReplies(self):
        self.no_replies = self.replies.count()


class Reply(models.Model):
    created = models.DateTimeField(
        auto_now_add=True
    )  # Field showing when tweet was created
    text = models.CharField(
        max_length=140, blank=True
    )  # Text content of tweet, max char count 140
    owner = models.ForeignKey(
        CustomUser, related_name="replies", on_delete=models.CASCADE
    )  # Each tweet is associated with a user
    tweet = models.ForeignKey(
        Tweet, related_name="replies", blank=True, null=True, on_delete=models.CASCADE
    )
