from django.urls import path

from . import views
urlpatterns = [

    path('resturanthome', views.resturant_home),
    path('add_resturant', views.add_resturant),
    path('resturant_store', views.resturant_store),
    path('my_resturant', views.my_resturant),
    path('logout', views.logout),

]