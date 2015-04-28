from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', include('recordlist.urls')),
    url(r'^recordlist/', include('recordlist.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'recordlist/', include('recordlist.urls')),
)
