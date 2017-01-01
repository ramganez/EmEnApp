from django.conf.urls import url
from django.views.generic.base import RedirectView, TemplateView

from enrollments.views import signin, signout, create_user_profile

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='signin'), name='go-to-signin'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^signout/$', signout, name='signout'),

    url(r'^register/$', create_user_profile, name='register'),

]
