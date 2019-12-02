from django.urls import path
from . import views

urlpatterns = [
    path('health-check/', views.health_check_api, name='health_check_api'),
    path('image-to-text/', views.image_to_text, name='image_to_text'),
    
]