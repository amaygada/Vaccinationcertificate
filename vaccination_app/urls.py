from django.urls import path
from .views import DetailsView

urlpatterns=[
    path('verify/',DetailsView.as_view(),name='data')
]