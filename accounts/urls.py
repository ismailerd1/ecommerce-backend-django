from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()
router.register('customer', views.CustomerViewSet)

urlpatterns = router.urls
