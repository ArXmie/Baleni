from django.contrib import admin
from .models import *
import hashlib

class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Если пароль не похож на хеш — хешируем
        if len(obj.password) != 64:
            obj.password = hashlib.sha256(obj.password.encode()).hexdigest()
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Size_Product)
admin.site.register(Product)
admin.site.register(Commission)
admin.site.register(Commission_Product)
admin.site.register(Product_Image)
