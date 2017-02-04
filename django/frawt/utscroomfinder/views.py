from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    about = open(os.path.join(BASE_DIR, "about.md"))
    about_list = [text for text in about.read().split("\n")]
    ver = open(os.path.join(BASE_DIR, "version.md")).read()
    title = open(os.path.join(BASE_DIR, "title.md")).read()
    template = loader.get_template("utscroomfinder/index.html")
    context = {
        'about_list': about_list,
        'prod_version': ver,
        'site_title': title,
    }
    return HttpResponse(template.render(context, request))
