from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'pipeline-object', views.PipelineObjectViewSet,
                basename='pipeline')
router.register(r'typeobject', views.TypeObjectViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]