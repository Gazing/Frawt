from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os

def index(request):
    about = open("about.md")
    about_list = [text for text in about.read().split("\n")]
    ver = open("version.md").read()
    title = open("title.md").read()
    template = loader.get_template("utscroomfinder/index.html")
    context = {
        'about_list': about_list,
        'prod_version': ver,
        'site_title': title,
    }
    return HttpResponse(template.render(context, request))
