from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    index = open("demo/index.html", "r")
    return HttpResponse(index.read())