# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from clients import views
import settings

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^getall/$', views.get_clients),
    url(r'^vote/$', views.get_vote_template),
    url(r'^vote/setvote/$', views.set_vote),
    url(r'^save/$', views.save_person),
    url(r'^delete/$', views.delete_person),
    url(r'^export/$', views.export_to_xls),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
