from cgitb import lookup
from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('order', views.OrderViewSet, basename='order')



urlpatterns = router.urls