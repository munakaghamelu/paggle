from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'paggle_home/home.html')

@login_required
def selectTask(request):
    return render(request, 'paggle_home/selectTask.html')

@login_required
def selectData(request):
    return render(request, 'paggle_home/selectData.html')

@login_required
def selectModel(request):
    return render(request, 'paggle_home/selectModel.html')

@login_required
def monitor(request):
    return render(request, 'paggle_home/monitor.html')

# Create your views here.
