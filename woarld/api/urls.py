from django.urls import path

from . import views

urlpatterns = [
    path('process-block', views.Detect.as_view()),
    path('history', views.Historical.as_view()),
    path('translate', views.Translate.as_view())
]
