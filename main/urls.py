from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('jokes', views.jokes, name='jokes'),
    path('vote/<int:joke_id>/', views.vote_joke, name='vote_joke'),
]