import csv
from curses import raw
from urllib import response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from .models import Dataset, ML_Model, HAM10000_Image, HAM10000_Metadata
import requests

def home(request):
    return render(request, 'paggle_home/home.html')

@login_required
def selectTask(request):
    return render(request, 'paggle_home/selectTask.html')

@login_required
def selectData(request):
    return render(request, 'paggle_home/selectData.html')

class DatasetListView(ListView):
    model = Dataset
    template_name= 'paggle_home/selectData.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'datasets'

class DatasetDetailView(DetailView):
    model = Dataset

class ModelCreateView(CreateView):
    model = ML_Model
    fields = ['raw_link']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def monitor(request):
    return render(request, 'paggle_home/monitor.html')

@login_required
def runModel(request):
    # Download the Data

    # This code is problematic, should only be run once database is populated
    # export the image data

    f = open('models/ham10000_metadata.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['lesion_id','image_id','dx','dx_type','age','sex','localization'])

    for meta in HAM10000_Metadata.objects.all().values_list('lesion_id','image_id','dx','dx_type','age','sex','localization'):
        writer.writerow(meta)

    f.close()

    # export the metadata
    f = open('models/ham10000_images.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['dataset','image_id','link','type'])

    for patient in HAM10000_Image.objects.all().values_list('dataset','image_id','link','type'):
        writer.writerow(patient)

    f.close()

    # Download the Model
    url = ML_Model.objects.all().values_list('raw_link')[0] # need to make this generic
    raw_link = str(url)
    raw_link = raw_link[2:-3]
    resp = requests.get(raw_link)
    f = open('models/user_model.py', 'wb').write(resp.content)

    # Run Model - 1) Run Python Script that contains key commands

    # Update results table with results.csv output
    
    return render(request, 'paggle_home/runModel.html')
