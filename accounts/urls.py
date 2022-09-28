from django.urls import path
from . import views

from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('customer', views.CustomerViewSet)

urlpatterns = router.urls