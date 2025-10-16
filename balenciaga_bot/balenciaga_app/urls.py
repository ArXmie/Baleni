from django.urls import path
from .views import *

urlpatterns = [
    path('test', root),
    path('mul', mul),
    path('umnoj', umnoj),
    path('delenie', delenie),
    path('index', index)
]