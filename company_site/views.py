import requests
from django.shortcuts import render


def home(request):
    return render(request, 'home.html')

def news(request, _=None):
    return render(request, 'news.html', {'subpath': _})

def management(request, _=None):
    return render(request, 'management.html', {'subpath': _})

def about(request, _=None):
    return render(request, 'about.html', {'subpath': _})

def contacts(request, _=None):
    return render(request, 'contacts.html', {'subpath': _})