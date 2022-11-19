from django.urls import path

from . import views

urlpatterns = [
    path('adminhome', views.adminhome),
    path('menu', views.menu),
    path('roles', views.roles),
    path('roles_store', views.role_store),
    path('role_delete/<int:pk>', views.delete_role, name="deleteRole"),
    path('register_store', views.register_store),
    path('categories', views.category_index),
    path('category_store', views.category_store),
    path('category_delete/<int:pk>', views.category_delete, name="deleteCategory"),
    path('category_edit/<str:pk>', views.category_edit),
    path('category_update', views.category_update),
    path('logout', views.logout),
    path('foodtypes', views.foodtype_index),
    path('foodtype_store', views.foodtype_store),
    path('foodtype_delete/<int:pk>', views.foodtype_delete, name="deleteFt"),
    path('foodtype_edit/<str:pk>', views.foodtype_edit),
    path('foodtype_update', views.foodtype_update),

    path('books', views.books_index),
    path('books_store', views.books_store),
    path('book_delete/<int:pk>', views.book_delete, name="deleteBook"),
    path('book_edit/<str:pk>', views.book_edit),
    path('book_update', views.book_update),

]