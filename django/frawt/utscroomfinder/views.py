from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    index = open("index.html", "r")
    return HttpResponse(index.read())

def send_rf_js(request):
    js = open("rf.js", "r")
    return HttpResponse(js.read())
