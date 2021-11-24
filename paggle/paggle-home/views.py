from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'paggle-home/home.html')

def selectTask(request):
    return render(request, 'paggle-home/selectTask.html')

def selectData(request):
    return render(request, 'paggle-home/selectData.html')

def selectModel(request):
    return render(request, 'paggle-home/selectModel.html')

def monitor(request):
    return render(request, 'paggle-home/monitor.html')

# Create your views here.
