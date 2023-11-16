from django.shortcuts import render
from django.http import HttpResponse

from .models import Tasks

def index(request):
    return HttpResponse("<a href='#'>Hello</a>")
