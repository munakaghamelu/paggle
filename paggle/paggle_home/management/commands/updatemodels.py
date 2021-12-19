from django.core.management.base import BaseCommand
import pandas as pd
from paggle_home.models import HAM10000_Metadata

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Database Connections
        df=pd.read_csv('encrypted_file.csv')
        for A,B,C,D,E,F,G in zip(df.lesion_id,df.image_id,df.dx,df.dx_type,df.age,df.sex,df.localization):
            models = HAM10000_Metadata(lesion_id=A,image_id=B,dx=C,dx_type=D,age=E,sex=F,localization=G)
            models.save()