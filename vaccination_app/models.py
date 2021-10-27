from django.db import models

# Create your models here.


class details(models.Model):
    sapId=models.CharField(max_length=20,primary_key=True)
    Full_vaccinate=models.BooleanField(default=False)
    Name=models.CharField(max_length=50)
    Age=models.IntegerField() 
    certificate=models.FileField(blank=False,null=True)
