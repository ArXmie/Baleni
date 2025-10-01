from django.shortcuts import render, HttpResponse
from .models import *

# Create your views here.
def root(request):
    test = request.GET['test']