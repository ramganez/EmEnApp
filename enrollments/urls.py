from django.conf.urls import url
from django.views.generic.base import RedirectView, TemplateView

from enrollments.views import signin, signout

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='signin'), name='go-to-signin'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^signout/$', signout, name='signout'),

]
