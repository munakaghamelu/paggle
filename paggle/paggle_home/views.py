import csv
from curses import raw
from email.policy import default
from urllib import response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, View
from django.urls import reverse
from sklearn.metrics import confusion_matrix
from .models import Dataset, ML_Model, HAM10000_Image, HAM10000_Metadata, Result
import requests
import subprocess
import plotly.express as px
import pandas as pd

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
    confusion_matrix = pd.read_csv('models/confusion_matrix.csv')
    metrics = pd.read_csv('models/metric_results.csv')

    cm_np = confusion_matrix.to_numpy()
    classes = cm_np[:,0:1]
    cm_np = cm_np[:,1:]
    class_label = classes.tolist()
    labels = []

    for c in class_label:
        str_c = str(c)
        labels.append(str_c[2:-2])

    matrix_plot_div = px.imshow(cm_np, 
                                labels=dict(x="Classes", 
                                            y="Classes", 
                                            color="Total Classifications"
                                            ),
                                x=labels,
                                y=labels,
                                text_auto=True)
    matrix_plot_div.update_xaxes(side="top")
    matrix = matrix_plot_div.to_html(full_html=False, default_height=500, default_width=700)
    context = {'matrix':matrix}
    return render(request, 'paggle_home/monitor.html', context)

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

class ExecuteDockerCompose(View):
    def get(self, request):
        # Execute docker-compose.yml
        subprocess.call(['docker-compose','-f', 'models/docker-compose.yml','up'])

        # store the outputs into result model table

        current_user = request.user.id
        current_model = ML_Model.objects.get(pk=1) # bug:this will be wrong, need to change if works
        result_df=pd.read_csv('models/metric_results.csv')
        confusion_matrix_df=pd.read_csv('models/confusion_matrix.csv')
        model = Result(current_user, current_model, result_df, confusion_matrix_df)
        model.save()

        # stop the docker container
        subprocess.call(['docker','stop','ham1000_model'])

        # Return - redirect back to page to load the results in plotly !!
        return HttpResponseRedirect(reverse("runModel.html"))