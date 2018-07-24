from django.urls import path
from . import views

urlpatterns = [
    path('AddEmp/',views.RenderPage,name = 'RenderPage'),
    path('Authentication/',views.GoogleAuth, name='GoogleAuth'),
    path('FinishAuth/', views.GetAuthToken, name='GetAuthToken'),
]
