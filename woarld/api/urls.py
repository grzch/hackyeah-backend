from django.urls import path

from . import views

urlpatterns = [
    path('process-block', views.Detect.as_view()),
]
