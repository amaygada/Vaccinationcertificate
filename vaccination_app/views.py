# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DetailSerializer
from .models import details
from  django.shortcuts import render
import requests
from rest_framework.decorators import api_view
import os
# Create your views here.
# class DetailsView(APIView):
@api_view(['GET','POST'])
def DetailsView(request):
    # def get(self,request):
    if request.method=="GET":
        d=details.objects.all()  
        serializer=DetailSerializer(d,many=True)
        return Response(serializer.data)

    if request.method=="POST":
        Detail_serializer=DetailSerializer(data=request.data)
        if Detail_serializer.is_valid():
            Detail_serializer.save()
            return Response(Detail_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(Detail_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def GetDetails(request,pk):
    if request.method=="GET":
        d=details.objects.get(sapId=pk)  
        serializer=DetailSerializer(d)
        return Response(serializer.data)

def input(request):
    if request.method=="POST":
        sapId=request.POST.get('sapId')
        Name=request.POST.get('Name')
        Age=request.POST.get('Age')
        certificate=request.POST.get('certificate')
        data={'sapId':sapId,'Name':Name,'Age':Age}
        files=[('certificate','application/pdf')]
        headers={}
        response=requests.request("POST",'http://127.0.0.1:8000/verif',headers=headers,data=data,files=files)
        return render(request,'index.html')
    else:
        return render(request,'index.html')

   
  
    # def post(self,request):