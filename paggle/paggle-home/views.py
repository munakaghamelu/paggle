from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'paggle-home/home.html')

@login_required
def selectTask(request):
    return render(request, 'paggle-home/selectTask.html')

@login_required
def selectData(request):
    return render(request, 'paggle-home/selectData.html')

@login_required
def selectModel(request):
    return render(request, 'paggle-home/selectModel.html')

@login_required
def monitor(request):
    return render(request, 'paggle-home/monitor.html')

# Create your views here.
