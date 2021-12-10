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
        self.name

class Model(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField(blank=True)
    link=models.TextField(blank=True)
    dataset= models.OneToOneField(Dataset, blank=True, null=True, on_delete=CASCADE)

    def __str__(self):
        f'{self.name} Works With {self.dataset.name} Dataset'

class Result(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    model = models.OneToOneField(Model, blank=True, null=True, on_delete=CASCADE)
    score = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.score} For Model {self.model.name}'

class Image(models.Model):
    # one to one relationship with metadata
    dataset = models.ForeignKey(Dataset, blank=True, null=True, on_delete=CASCADE)
    image_id=models.CharField(max_length=50)
    link=models.CharField(max_length=100)
    type=models.CharField(max_length=10)

    def __str__(self):
        f'{self.id} From {self.dataset.name} Dataset'

class HAM10000_Metadata(models.Model):
    lesion_id=models.CharField(max_length=50)
    image_id=models.OneToOneField(Image, blank=True, null=True, on_delete=CASCADE)
    dx=models.CharField(max_length=10)
    dx_type=models.CharField(max_length=10)
    age=models.DecimalField(decimal_places=1, max_digits=5)
    sex=models.CharField(max_length=50)
    localization=models.CharField(max_length=50)

    def __str__(self):
        f'Lesion ID {self.lesion_id}'
