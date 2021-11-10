from rest_framework import serializers
from .models import details


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def data(self):
        return {
            "file": self._validated_data["file"],
        }


    

# class DataSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Data
#         fields=['sapId','certificate1','certificate2']

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=details
        fields=['sapId', 'Name', 'Age', 'certificate'] 