from rest_framework import serializers
from .models import details

# class DataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Data
#         fields=['sapId','certificate1','certificate2']

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=details
        fields=['sapId','Full_vaccinate','Name','Age','certificate']