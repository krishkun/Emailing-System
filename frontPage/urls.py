from django.urls import path
from . import views

urlpatterns = [
    path('',views.RenderPage, name = 'RenderPage')
]
