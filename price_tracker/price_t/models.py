from django.db import models

# Create your models here.
class Products(models.Model):
    id=models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_url= models.URLField(unique=True)
    product_price = models.CharField(max_length=10)
    email= models.CharField(max_length=50)
