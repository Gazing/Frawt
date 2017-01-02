from django.shortcuts import render
from django.http import HttpResponse
import os

def index(request):
    index = open("/static/live/index.html", "r")
    return HttpResponse(index.read())
