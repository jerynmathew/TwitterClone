from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tweet(models.Model):
    content = models.CharField(max_length=140)
    posted_on = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        msg = "<Tweeted at {datetime}: {tweet}...>".format(datetime=self.posted_on.strftime("%H:%M:%S on %a, %d %b %Y"), tweet=self.content[0:50])
        return msg

    def get_hashtag(self):
        result = None
        try:
            import re
            result = re.findall("(?P<hash>#\w+)\s*", self.content)
            result = result if result else None
        except:
            result = None

        return result

    def get_info(self):
        result = {
            'id': self.id,
            'posted_on': self.posted_on,
            "owner": self.owner.username
        }

        return result


    class Meta:
        ordering = ['-posted_on']


