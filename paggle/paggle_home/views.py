from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from .models import Dataset, ML_Model

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
    fields = ['name','description','imports','dataset_class', 'preprocess_function', 'createModel_function', 'train_function', 'test_function']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required
def monitor(request):
    return render(request, 'paggle_home/monitor.html')

@login_required
def runModel(request):
    return render(request, 'paggle_home/runModel.html')
# needs to receive data as a form


# Create your views here.
