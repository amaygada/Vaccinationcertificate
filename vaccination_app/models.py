from django.db import models
from django.db.models import fields

# Create your models here.


class details(models.Model):
    YEAR_LIST = [("FE", "FE"), ("SE", "SE"), ("TE", "TE"), ("BE", "BE")]
    GENDER_LIST = [("male", "male"), ("female", "female"), ("other", "other")]
    DEP_LIST = ["CS", "IT", "Elex", "EXTC", "Chemical", "Production", "Mechanical", "Biomedical", "Data Science", "Ai-ML", "AI-DS", "IOT and Cyber Security with Blockchain"]
    
    sapId=models.CharField(max_length=20,primary_key=True)
    full_vaccinate=models.BooleanField(default=False)
    name=models.CharField(max_length=50)
    age=models.IntegerField(null=False) 
    gender = models.CharField(null=False, choices=GENDER_LIST, max_length=10)
    department = models.CharField(null=False, max_length=30)
    year = models.CharField(null=False, choices=YEAR_LIST, max_length=5)
    folder_id = models.CharField(null=False, max_length=40)

    def __str__(self):
        return self.sapId
    # certificate=models.FileField(blank=False,null=True)
