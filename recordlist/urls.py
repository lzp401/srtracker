__author__ = 'luz'

from django.conf.urls import patterns, url
from recordlist import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^markreview/$', views.markreview, name='markreview'),
    url(r"^(?P<recordid>[0-9]+)/$", views.detail, name='detail'),
    url(r"^(?P<recordid>[0-9]+)/update$", views.update, name='update'),
)