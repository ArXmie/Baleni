from django.urls import path
from .views import *

urlpatterns = [
    path('test', root),
    path('mul', mul),
    path('umnoj', umnoj),
    path('delenie', delenie),
    path('', index, name='home'),
    path('search/', search, name='search'),
    path('product/<int:product_id>/', template_product, name='product')
]