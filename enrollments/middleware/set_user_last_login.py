from django.utils.timezone import now
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class SetUserLastLoginMiddleware(object):
    
    def process_response(self, request, response):
        if request.user.is_authenticated():
            # Update last login time after request finished processing.
            user_obj = get_object_or_404(User, pk=request.user.pk)
            prof_obj = user_obj.profile
            prof_obj.last_visit = now()
            prof_obj.save()

        return response