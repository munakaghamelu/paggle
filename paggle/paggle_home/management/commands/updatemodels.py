from django.core.management.base import BaseCommand
import pandas as pd
from paggle_home.models import Dataset, HAM10000_Image, HAM10000_Metadata, Dataset
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from django.core import serializers

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #Database Connections
        df=pd.read_csv('ingest_data/ham10000_metadata.csv')
        for A,B,C,D,E,F,G in zip(df.lesion_id,df.image_id,df.dx,df.dx_type,df.age,df.sex,df.localization):
            models = HAM10000_Metadata(lesion_id=A,image_id=B,dx=C,dx_type=D,age=E,sex=F,localization=G)
            models.save()

        df=pd.read_csv('ingest_data/datasets.csv')
        for A,B,C,D in zip(df.name,df.description,df.num_of_images,df.date_added):
            models = Dataset(name=A,description=B,num_of_images=C,date_added=parse_datetime(D))
            models.save()

        df=pd.read_csv('ingest_data/ham10000_images.csv')
        dataset_query_set = Dataset.objects.get(name__icontains='HAM10000')
        for A,B,C in zip(df.image_id,df.link,df.type):
            # get id of dataset
            models = HAM10000_Image(dataset=dataset_query_set,image_id=A,link=B,type=C)
            models.save()
