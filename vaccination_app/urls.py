from django.urls import path
from .views import DetailsView, CheckView
from . import views

urlpatterns=[
    path('details/',DetailsView.as_view(), name='details'),
    path('check/', CheckView.as_view(), name="check")
]