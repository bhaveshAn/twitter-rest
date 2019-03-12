from django.contrib import admin

from tweet.models import Tweet
# Register your models here.

admin.site.register(Tweet) #Allow tweet to be editable on admin end
