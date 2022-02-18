from django.db import models
from numpy import blackman
from users.models import Profile
from django.db.models.deletion import CASCADE
from django.db.models.fields import BLANK_CHOICE_DASH
from django.urls import reverse

# Create your models here.
class Dataset(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    num_of_images=models.IntegerField()
    date_added=models.DateTimeField()

    def __str__(self):
        return self.name

class ML_Model(models.Model):
    name=models.CharField(max_length=100, blank=False)
    description=models.CharField(max_length=200, blank=False)
    imports=models.TextField(blank=False)
    dataset_class=models.TextField(blank=False)
    preprocess_function=models.TextField(blank=False)
    createModel_function=models.TextField(blank=False)
    train_function=models.TextField(blank=False)
    test_function=models.TextField(blank=False)

    def __str__(self):
        return f'{self.name} to preform {self.description}'

    # redirect page after model has been created, use reverse instead
    def get_absolute_url(self):
        return reverse('paggle-runModel', kwargs={})

class Result(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    model = models.OneToOneField(ML_Model, blank=True, null=True, on_delete=CASCADE)
    score = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.score} For Model {self.model.name}'

class HAM10000_Metadata(models.Model):
    lesion_id=models.TextField(null=True)
    image_id=models.TextField(null=True)
    dx=models.TextField(null=True)
    dx_type=models.TextField(null=True)
    age=models.TextField(null=True)
    sex=models.TextField(null=True)
    localization=models.TextField(null=True)

    def __str__(self):
        return f'Lesion ID {self.lesion_id}'

class HAM10000_Image(models.Model):
    # one to one relationship with metadata
    dataset=models.ForeignKey(Dataset, blank=True, null=True, on_delete=CASCADE)
    image_id=models.CharField(max_length=100)
    link=models.CharField(max_length=100)
    type=models.CharField(max_length=10)

    def __str__(self):
        return f'{self.id} From {self.dataset.name} Dataset'
