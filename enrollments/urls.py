from django.conf.urls import url
from django.views.generic.base import RedirectView, TemplateView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='signin'), name='go-to-signin'),
    url(r'^signin/$', TemplateView.as_view(template_name='base.html'), name='signin'),

]
