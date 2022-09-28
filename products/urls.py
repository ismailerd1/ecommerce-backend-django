from cgitb import lookup
from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('order', views.OrderViewSet)

order_items_router = routers.NestedDefaultRouter(router, 'order', lookup='order')
order_items_router.register('items', views.OrderItemViewSet, basename='order-items')


urlpatterns = router.urls + order_items_router.urls