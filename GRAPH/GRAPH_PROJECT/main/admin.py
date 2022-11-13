
from django.contrib import admin
from main.models import FigureImage
# Register your models here.



class FigureImageAdmin(admin.ModelAdmin):
    list_display = ('figure', 'graph')


    
admin.site.register(FigureImage, FigureImageAdmin)
