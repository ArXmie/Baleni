from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(Size_Product)
admin.site.register(Commission)
admin.site.register(Commission_Product)
