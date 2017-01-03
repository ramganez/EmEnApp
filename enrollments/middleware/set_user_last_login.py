from django.utils.timezone import now
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from enrollments.models import Profile

class SetUserLastLoginMiddleware(object):

    def process_response(self, request, response):
        if request.user.is_authenticated():
            # Update last login time after request finished processing.
            user_obj = get_object_or_404(User, pk=request.user.pk)
            prof_obj = user_obj.profile
            Profile.objects.filter(user=user_obj).update(last_visit=now())
        return response