from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'paggle-home/home.html')

def selectData(request):
    return render(request, 'paggle-home/selectData.html')

def login(request):
    return render(request, 'paggle-home/login.html')

def register(request):
    return render(request, 'paggle-home/register.html')

def monitor(request):
    return render(request, 'paggle-home/monitor.html')

# Create your views here.
