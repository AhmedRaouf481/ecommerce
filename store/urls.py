from django.contrib import admin
from django.urls import path
from . import views

 


urlpatterns = [
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutPage, name = 'logout'),
    path('register/', views.registerPage, name = 'register'),
    path('', views.home, name = 'home'),
    path('profile/', views.profile, name = 'profile'),
    path('aboutus/', views.aboutus, name = 'aboutus'),
    path('cart/', views.cart, name = 'cart'),

    #API
    path('cartListAPI/', views.cartDataAPI),


    path('update_item/', views.updateItem, name = 'update_item'),
    path('delete_item/', views.deleteItem, name = 'delete_item'),
    path('edit_quantity/', views.editqty, name = 'edit_quantity'),
    
    path('create_product/', views.createProduct, name = 'create_product'),
    path('edit_product/<str:pk>/', views.editProduct, name = 'edit_product'),
    path('delete_product/<str:pk>/', views.deleteProduct, name = 'delete_product'),


    path('product/<str:pk>/', views.product, name = 'product'),

    
]