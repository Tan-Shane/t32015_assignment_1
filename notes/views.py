from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from .models import Note
import re
from django.db.models import Q


# Create your views here.# Create your views here.

def main(request):
    allnotes = Note.objects.all()
    return render(request, 'notes/main.html', {'notes': allnotes})  

def notes_list(request, folder):
        allnotes = Note.objects.filter(folder__title__iexact=folder)
        total = allnotes.count();
        return render(request, 'notes/index.html', {'notes': allnotes, 'total':total, 'day':str(folder).capitalize()})  

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
def note(request, note_id):
    note = Note.objects.get(id=note_id)   
    return render(request, 'notes/note.html', {'note':note})
