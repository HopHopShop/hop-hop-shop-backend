from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ListCategories

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("products", ProductViewSet)

urlpatterns = [
    path("categories/all/", ListCategories.as_view(), name="all_categories"),
    path("", include(router.urls)),
]
