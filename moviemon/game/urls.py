from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('worldmap/', views.worldmap),
    path('battle/<str:movie_id>', views.battle),
    path('options/save_game/', views.options_save),
    path('options/load_game/', views.options_load),
    path('options/', views.options),
    path('moviedex/', views.moviedex),
    path('moviedex/<str:movie_id>', views.detail)
]
