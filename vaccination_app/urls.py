from django.urls import path
# from .views import DetailsView
from . import views

urlpatterns=[
    path('',views.input,name='input'),
    path('verif',views.DetailsView,name='Data'),
    path('details/<str:pk>',views.GetDetails,name='Details')
]