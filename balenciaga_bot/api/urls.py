from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'size-products', SizeProductViewSet)
router.register(r'commissions', CommissionViewSet)
router.register(r'commission-products', CommissionProductViewSet)

urlpatterns = router.urls