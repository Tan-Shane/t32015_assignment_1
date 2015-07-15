from django.conf.urls import patterns, include, url
from django.contrib import admin
from notes import views

urlpatterns = patterns('',
    url(r'^index/(?P<folder>.*)$', views.notes_list, name='index'),
    url(r'^main/', views.main, name='main'),
    url(r'^note/(?P<note_id>\d+)$', views.note, name='detail'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
)