from .models import Tweet
from .forms import TweetForm
from apps.accounts.models import UserProfile
from django.views.generic.base import View
from django.utils import simplejson as json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger('logview.tweet')


def JSONResponse(response_object):
    '''
    Returns a HTTP Response object with json type response.
    response_object: Dictionary object to jsonify
    '''
    from django.shortcuts import HttpResponse
    return HttpResponse(
                            content=json.dumps(
                                                    response_object, 
                                                    indent=3, 
                                                    cls=DjangoJSONEncoder
                                              ), 
                            content_type='application/json'
                       )
    

class TweetView(View):
    def get(self, request, *args, **kwargs):
        response = {
                        'status': 'failed',
                        'message': 'Default error message',
                        'code': -1
                    }
        try:
            # Fetch top results
            top_post = request.session.get('top_post', None)
            results = self.get_top_posts(request, top_post)

            # Set the session variables
            request.session['top_post'] = results[0]['posted_on']
            request.session['last_post'] = results[-1]['posted_on']

            # Prepare the response
            response = {
                            'status': 'success',
                            'message': results,
                            'code': 1
                        }
        except:
            response['message'] = u'Unknown error occurred!'
            logger.exception('Unknown exception in TweetView GET request!')

        return JSONResponse(response)

    def get_top_posts(self, request, last_date=None):
        # Get follows list
        follows = UserProfile.objects.get(user=request.user).follows.all()
        follows.append(request.user)
        if not last_date:
            results = Tweet.objects.filter(owner__in=follows).order_by('-posted_on').values('content', 'posted_on', 'owner')
        else:
            results = Tweet.objects.filter(owner__in=follows, posted_on__gte=last_date).order_by('-posted_on').values('content', 'posted_on', 'owner')

        # Always return top 20 results
        return results[:20]

    def post(self, request, *args, **kwargs):
        response = {
                        'status': 'failed',
                        'message': 'Default error message',
                        'code': -1
                    }

        form = TweetForm(request.POST)

        try:
            if form.is_valid():
                form.save(request.user)

                response = {
                                'status': 'success',
                                'message': form.cleaned_data,
                                'code': 1
                           }

            else:
                response['message'] = form.errors
                logger.error('Error in Form POST. Errors = {errors}'.format(errors=form.errors))

        except:
            response['message'] = u"Unknown Exception during TweetView POST request"
            logger.exception('Unknown Exception during TweetView POST request')

        return JSONResponse(response)

        @method_decorator(login_required)
        def dispatch(self, request, *args, **kwargs):
            return super(TweetView, self).dispatch(request, *args, **kwargs)

