from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def Homepage(request):
     template = loader.get_template('index.html')
     return HttpResponse(template.render())

def Abhishek(request):
     template = loader.get_template('index.html')
     return HttpResponse(template.render())

def Hello(request):
    return HttpResponse("Hello world!")