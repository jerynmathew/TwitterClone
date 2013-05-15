from django import forms
from .models import Tweet

class TweetForm(forms.Form):
    content = forms.CharField(max_length=140)

    def save(self, user):
        tweet = Tweet(
                        content=self.cleaned_data['content'],
                        owner=user
                     )

        tweet.save()
        return tweet


