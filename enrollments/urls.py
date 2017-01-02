from django.conf.urls import url
from django.views.generic.base import RedirectView, TemplateView

from enrollments.views import (signin, signout, create_user_profile,
                               dashboard_view, update_user_profile)

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='signin'), name='go-to-signin'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^signout/$', signout, name='signout'),

    url(r'^register/$', create_user_profile, name='register'),
    url(r'^profile/(?P<username_id>[\w-]+)/update$', update_user_profile, name='profile_update'),
    url(r'^profile/(?P<username_id>[\w-]+)$', dashboard_view, name='profile'),
    ]
