from django.urls import path
from .views import *

urlpatterns = [
    path('test', root),
    path('mul', mul),
    path('umnoj', umnoj),
    path('delenie', delenie),
    path('', index, name='home'),
    path('product', template_product, name='product')
]