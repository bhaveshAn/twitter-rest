"""twitterBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import tweet.views
import user.views

import rest_framework.authtoken.views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^new-tweet/$',tweet.views.TweetPost.as_view()), # POST (Creates new tweet)
    url(r'^tweets/$',tweet.views.TweetList.as_view()), # GET (Lists all the tweets)
    url(r'^tweets/(?P<pk>[0-9]+)/$',tweet.views.TweetDetail.as_view()), # GET (Details about a tweet)
    url(r'^new-user/$',user.views.UserCreate.as_view()), # POST (Creates new user)
    url(r'^user/$',user.views.UserList.as_view()), # GET (Lists the users)
    url(r'^user/(?P<username>[\w]+)/$',user.views.UserDetail.as_view()), # GET (Details about a user)
    url(r'^user/(?P<username>[\w]+)/tweets/$',tweet.views.UserTweets.as_view()), # GET (Lists the user's tweets)
    url(r'^tweets/(?P<pk>[0-9]+)/reply/$',tweet.views.ReplyTweetPost.as_view()), # POST (Creates replies for a tweet)
    url(r'^tweets/(?P<pk>[0-9]+)/like/$',tweet.views.LikeTweet.as_view()), # PUT (favourate a tweet)
    url(r'^user/(?P<username>[\w]+)/follow/$',user.views.UserFollow.as_view()), # PUT (Follow a user)
    url(r'^login/', rest_framework.authtoken.views.obtain_auth_token), # POST (returns Token)
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace = 'rest_framework'))
]
urlpatterns = format_suffix_patterns(urlpatterns)
