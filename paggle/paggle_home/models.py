from django.db import models
from users.models import Profile
from django.db.models.deletion import CASCADE
from django.db.models.fields import BLANK_CHOICE_DASH

# Create your models here.
class Dataset(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    num_of_images=models.IntegerField()
    date_added=models.DateTimeField()

    def __str__(self):
        return self.name

class Model(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField(blank=True)
    link=models.TextField(blank=True)
    dataset= models.OneToOneField(Dataset, blank=True, null=True, on_delete=CASCADE)

    def __str__(self):
        return f'{self.name} Works With {self.dataset.name} Dataset'

class Result(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    model = models.OneToOneField(Model, blank=True, null=True, on_delete=CASCADE)
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
    image_id=models.OneToOneField(HAM10000_Metadata, blank=True, null=True, on_delete=CASCADE)
    link=models.CharField(max_length=100)
    type=models.CharField(max_length=10)

    def __str__(self):
        return f'{self.id} From {self.dataset.name} Dataset'
