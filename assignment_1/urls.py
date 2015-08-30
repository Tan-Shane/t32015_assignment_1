from django.conf.urls import patterns, include, url
from django.contrib import admin
from notes import views
from django.views.generic import ListView, DetailView, DeleteView
from notes.models import Note


urlpatterns = patterns('',
    url(r'^main/', views.main, name='main'),
    url(r'^listall/$', ListView.as_view(model=Note)),
    #url(r'^index/(?P<folder>.*)$', views.notes_list, name='index'),
    url(r'^list/(?P<folder>.*)$', views.NoteList.as_view(), name='notes_list'),
    #url(r'^detail/(?P<pk>\d+)$', DetailView.as_view(model=Note), name='detail'),
    url(r'^note/(?P<pk>\d+)$', views.NoteDetail.as_view(),  name='detail'),
    #url(r'^note/(?P<note_id>\d+)$', views.note, name='detail'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^add/$', views.NoteCreate.as_view(), name='note_add'),
    url(r'^note/(?P<pk>\d+)/edit/$', views.NoteUpdate.as_view(),  name='note_update'),
    url(r'^delete/(?P<pk>\d+)$', views.NoteDelete.as_view(), name='note_delete'),
)