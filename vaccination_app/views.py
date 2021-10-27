# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DetailSerializer
from .models import details

# Create your views here.

class DetailsView(APIView):
    def get(self,request):
        d=details.objects.all()
        serializer=DetailSerializer(d,many=True)
        return Response(serializer.data)

    def post(self,request):
        Detail_serializer=DetailSerializer(data=request.data)
        if Detail_serializer.is_valid():
            Detail_serializer.save()
            return Response(Detail_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(Detail_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
