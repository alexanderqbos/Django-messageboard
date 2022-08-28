from django.urls import path
from . import views

urlpatterns = [
    path('get/<str:key>/', views.get_message, name='get_message'), # set url for get view
    path('create/', views.create_message, name='create_message'), # set url for create view
    path('', views.index, name='index'), # set url for index view
    path('update/<str:key>/', views.update_message, name='update_message') # set url for update view
]