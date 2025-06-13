from rest_framework.routers import DefaultRouter
from app_store.views import CategoryViewSet, ProductViewSet
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)

urlpatterns = router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)