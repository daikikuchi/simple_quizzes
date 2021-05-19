from django.urls import path, include
from rest_framework.routers import DefaultRouter

from question import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)

app_name = 'question'

urlpatterns = [
    path('', include(router.urls))
]
