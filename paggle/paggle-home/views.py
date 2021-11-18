from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Paggle Home</h1>')

def selectData(request):
    return HttpResponse('<h1>Select Dataset and Model</h1>')

def login(request):
    return HttpResponse('<h1>Login User</h1>')

def register(request):
    return HttpResponse('<h1>Register User</h1>')

def monitor(request):
    return HttpResponse('<h1>ML Monitoring System</h1>')

# Create your views here.
