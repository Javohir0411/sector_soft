from rest_framework.routers import DefaultRouter
from app_store.views import CategoryViewSet, ProductViewSet, ProductColorViewSet, ProductImageViewSet
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)
router.register("product_color", ProductColorViewSet)
router.register("product_image", ProductImageViewSet)

urlpatterns = router.urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)