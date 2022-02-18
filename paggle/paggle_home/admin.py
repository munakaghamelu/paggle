from django.contrib import admin
from .models import Dataset
from .models import ML_Model
from .models import Result
from .models import HAM10000_Image
from .models import HAM10000_Metadata

# Register your models here.
admin.site.register(Dataset)
admin.site.register(ML_Model)
admin.site.register(Result)
admin.site.register(HAM10000_Image)
admin.site.register(HAM10000_Metadata)
