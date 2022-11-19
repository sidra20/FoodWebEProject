from django.urls import path

from . import views
urlpatterns = [

    path('resturanthome', views.resturant_home),

]