# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DetailSerializer, FileSerializer
from .models import details
from  django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from verify_module import verify
from rest_framework.parsers import MultiPartParser, JSONParser, FileUploadParser
from drive_module import drive
import os


'''
# a call to get details from students
# use a file serializer to get certificate in that same call
# read file and see if fully vaccinated
# if fully vaccinated, add to drive to appropriate drive folders
'''
class DetailsView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        key_req = ["name", "sap", "age", "gender", "department", "year", "file"]
        for i in list(request.data.keys()):
            if i not in key_req:
                return Response({"data" : {"val":False, "detail":"Invalid request parameters"}}, status=status.HTTP_400_BAD_REQUEST)

        name = request.data["name"]
        sap = request.data["sap"]
        age = request.data["age"]
        gender = request.data["gender"]
        dep = request.data["department"]
        year = request.data["year"]

        already_exists = details.objects.filter(sapId=sap)
        if len(already_exists)>0:
            return Response({"data" : {"val":False, "detail" : "already submitted once."}}, status=status.HTTP_400_BAD_REQUEST)

        d = {}
        d["file"] = request.data["file"]
        serializer = FileSerializer(data=d)
        if serializer.is_valid():

            verified = verify.verify(request.data["file"], sap)
            if verified["val"] == False:
                return Response({"data" : {"val":verified["val"], "detail" : verified["details"]}}, status=status.HTTP_400_BAD_REQUEST)


            #verify if incoming details same as in the pdf
            data = verified["details"]["data"]
            flag = True
            
            if int(data["age"][0])>24:
                return Response({"data" : {"val":False, "detail" : "Age in certificate is too high for a student."}}, status=status.HTTP_400_BAD_REQUEST)
            
            if int(data["age"][0])<18:
                return Response({"data" : {"val":False, "detail" : "Age in certificate is too low for a student."}}, status=status.HTTP_400_BAD_REQUEST)

            #name
            name_ = name.lower().split()
            for i,j in zip(name_,data["name"]):
                if(i!=j):
                    # print("name error")
                    flag = False 
                    break 
            #age
            if str(age)!=data["age"][0]:
                # print("age error")
                flag=False
            
            # print(data)
            # print(name_)
            # print(age, str(age))

            if flag==False:
                return Response({"data" : {"val":False, "detail" : "Certificate details don't match form details."}}, status=status.HTTP_400_BAD_REQUEST)

            #add to drive
            im_path = verified["details"]["im_path"]
            s = drive.add_folder(sap, dep, year)
            drive.add_file(im_path, s["id"], sap)

            #save all data to model
            details.objects.create(
                name = name,
                sapId = sap,
                full_vaccinate = True,
                age = age,
                gender = gender,
                department = dep,
                year = year,
                folder_id = s["id"] 
            )

            return Response({"data" : {"val":True, "detail" : "Success"}}, status=status.HTTP_200_OK)
        return Response({"data" : {"val" : False, "detail" : serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)


class CheckView(APIView):
    def post(self, request, format=None):
        key_req = ["sap"]
        for i in list(request.data.keys()):
            if i not in key_req:
                return Response({"data" : {"val":False, "detail":"Invalid request parameters"}}, status=status.HTTP_400_BAD_REQUEST)
        
        sap = request.data["sap"]
        allowed = details.objects.filter(sapId=sap)
        if len(allowed)==0:
            return Response({"data" : {"val":False, "detail":"Not double vaccinated"}}, status=status.HTTP_400_BAD_REQUEST)
        
        d = {}
        d["name"] = allowed[0].name
        d["age"] = allowed[0].age 
        d["gender"] = allowed[0].gender 
        d["department"] = allowed[0].department 
        d["year"] = allowed[0].year 
        d["sap"] = allowed[0].sapId
        d["link to certificate"] = "https://drive.google.com/drive/u/1/folders/" + allowed[0].folder_id
        return Response({"data" : {"val":True, "detail" : d}}, status=status.HTTP_200_OK)

# Create your views here.
# class DetailsView(APIView):
# @api_view(['GET','POST'])
# def DetailsView(request):
#     # def get(self,request):
#     if request.method=="GET":
#         d=details.objects.all()  
#         serializer=DetailSerializer(d,many=True)
#         return Response(serializer.data)

#     if request.method=="POST":
#         Detail_serializer=DetailSerializer(data=request.data)
#         if Detail_serializer.is_valid():
#             Detail_serializer.save()
#             return Response(Detail_serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(Detail_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# def GetDetails(request,pk):
#     if request.method=="GET":
#         d=details.objects.get(sapId=pk)  
#         serializer=DetailSerializer(d)
#         return Response(serializer.data)

# def input(request):
#     if request.method=="POST":
#         sapId=request.POST.get('sapId')
#         Name=request.POST.get('Name')
#         Age=request.POST.get('Age')
#         certificate=request.POST.get('certificate')
#         data={'sapId':sapId,'Name':Name,'Age':Age}
#         files=[('certificate','application/pdf')]
#         headers={}
#         response=requests.request("POST",'http://127.0.0.1:8000/verif',headers=headers,data=data,files=files)
#         return render(request,'index.html')
#     else:
#         return render(request,'index.html')