from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from .models import Note
import re
from django.db.models import Q
from django.views.generic import ListView, DetailView, DeleteView, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from notes.forms import NoteForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.models import UserProfile
import json

class NoteCreate(CreateView):
    model = Note
    form_class = NoteForm

class NoteUpdate(UpdateView):
    model = Note
    form_class = NoteForm
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NoteUpdate, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(NoteUpdate, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context


class NoteDelete(DeleteView):
    model = Note
    success_url = '/list/'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NoteDelete, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(NoteDelete, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context
    

class NoteByTag(ListView):
    model = Note
    
    queryset = Note.objects.all()
    def get_queryset(self):
        tags = self.kwargs['tags']
        pieces = tags.split('/') #extract different tags separated by /
        
        queries = [Q(tag__title__iexact=value) for value in pieces]
        # Take one Q object from the list
        query = queries.pop()
        # Or the Q object with the ones remaining in the list
        for item in queries:
            query |= item
        # Query the model
        curruser = UserProfile.objects.filter(user=self.request.user) #only query notes by curruser
        allnotes = Note.objects.filter(user=curruser).filter(query).distinct().order_by('tag__title')
        self.queryset = allnotes #Setting the queryset to allow get_context_data to apply count
        return allnotes
    
    def get_context_data(self, **kwargs):
        context = super(NoteByTag, self).get_context_data(**kwargs)
        context['total'] = self.queryset.count()
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context




# Create your views here.# Create your views here.

class NoteDetail(DetailView):
    model = Note
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NoteDetail, self).dispatch(*args, **kwargs)
        
    def get_context_data(self, **kwargs):
        context = super(NoteDetail, self).get_context_data(**kwargs)
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context


class NoteDelete(DeleteView):
    model = Note
    template_name = 'notes/note_delete.html'
    def get_success_url(self):
        return reverse('main')
    

class NoteList(ListView):
    #https://docs.djangoproject.com/en/1.7/topics/class-based-views/generic-display/
    model = Note
    queryset = Note.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NoteList, self).dispatch(*args, **kwargs)
        
    def get_queryset(self):
        #self.request.user will contain the "User" object, however,
        #user field in the Note model is an instance of "UserProfile" object
        #So need to ensure that when we filter all the user owned notes, we
        #filter using the 'correct' UserProfile instance based on logged in "User" object 
        #in self.request.user
        curruser = UserProfile.objects.get(user=self.request.user)
        folder = self.kwargs['folder']
        if folder == '':
            #filter based on current logged in user
            self.queryset = Note.objects.filter(user=curruser)
            return self.queryset
        else:
            #filter based on current logged in user
            self.queryset = Note.objects.all().filter(user=curruser).filter(folder__title__iexact=folder)
            return self.queryset
    
    
    def get_context_data(self, **kwargs):
        context = super(NoteList, self).get_context_data(**kwargs)
        context['total'] = self.queryset.count()
        #provided so that the avatar can be displayed in base.html
        context['curruser'] = UserProfile.objects.get(user=self.request.user)
        return context
"""
    def get_queryset(self):
        folder = self.kwargs['folder']
        if folder == '':
            return Note.objects.all()
        else:
            return Note.objects.filter(folder__title__iexact=folder)"""
            
    

def main(request):
    allnotes = Note.objects.all()
    return render(request, 'notes/main.html', {'notes': allnotes})  

def notes_list(request, folder):
        allnotes = Note.objects.filter(folder__title__iexact=folder)
        total = allnotes.count();
        return render(request, 'notes/index.html', {'notes': allnotes, 'total':total, 'day':str(folder).capitalize()})  

def note(request, note_id):
    note = Note.objects.get(id=note_id)   
    return render(request, 'notes/note.html', {'note':note})

def notes_tags(request, tags):
    pieces = tags.split('/')
    # allnotes = Note.objects.none() #required when doing normal filter pipe query ... see below
    for p in pieces:
        #This is to combine results from different querysets from SAME model using normal pipe
        #https://groups.google.com/forum/#!topic/django-users/0i6KjzeM8OI
        #If the querysets are from different models, have to use itertools
        #http://chriskief.com/2015/01/12/combine-2-django-querysets-from-different-models/
        #allnotes = allnotes | Note.objects.filter(tag__title__iexact=p) # can have duplicates ... need another method
        
        #http://stackoverflow.com/questions/852414/how-to-dynamically-compose-an-or-query-filter-in-django
        # Turn list of values into list of Q objects
        queries = [Q(tag__title__iexact=value) for value in pieces]
        # Take one Q object from the list
        query = queries.pop()
        # Or the Q object with the ones remaining in the list
        for item in queries:
            query |= item
        # Query the model
        allnotes = Note.objects.filter(query).distinct().order_by('tag__title__iexact')
        total = allnotes.count();
    return render(request, 'notes/index.html', {'pieces':pieces, 'notes': allnotes, 'total':total})   


"""def note(request, note_id):
    note = Note.objects.get(id=note_id)
    responsetext = ""
    responsetext += "<h1>" + str(note.id) + "</h1>"
    responsetext += "<h2>" + note.title + "</h2>"
    responsetext += "<h2>" + note.content + "</h2>"
    return HttpResponse(responsetext)
"""

