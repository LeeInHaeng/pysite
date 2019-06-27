from django.http import HttpResponse
from django.shortcuts import render
import json


def index(request):
    return render(request, 'bs/main/index.html')


def redirect(request):
    return render(request, 'main/redirect.html')