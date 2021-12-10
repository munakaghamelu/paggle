from django.contrib import admin
from .models import Dataset
from .models import Model
from .models import Result
from .models import Image
from .models import HAM10000_Metadata

# Register your models here.
admin.site.register(Dataset)
admin.site.register(Model)
admin.site.register(Result)
admin.site.register(Image)
admin.site.register(HAM10000_Metadata)
