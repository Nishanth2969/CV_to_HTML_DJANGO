from django.urls import path
from .views import cv_view, remove_cv

urlpatterns = [
    path('', cv_view, name='home'),        # Home page route
    path('cv/', cv_view, name='cv'),
    path('cv/remove/', remove_cv, name='remove_cv'),
]
