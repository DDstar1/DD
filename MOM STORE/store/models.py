from django.db import models

# Create your models here.

class Products(models.Model):
    description = models.TextField()
    title = models.CharField(max_length=63)  
     

    