from django.conf.urls.defaults import patterns, url
from .views import TweetView

urlpatterns = patterns('apps.accounts.views',
    url(
            r'^$', TweetView.as_view(), name='tweet'
        )
)
