from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('products', views.ProductViewSet)
router.register('cart', views.CartViewSet, basename='cart')
router.register('order', views.OrderViewSet, basename='order')


cart_item_router = routers.NestedDefaultRouter(router, 'cart', lookup='cart')
cart_item_router.register('items', views.CartItemViewSet, basename='items')


urlpatterns = router.urls + cart_item_router.urls
