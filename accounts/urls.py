from django.urls import path
from .views import *

from django.contrib.auth import views as auth_views

urlpatterns = [

    path('register/', registerPage, name="register"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),

    path('', home, name="home"),
    path('user/', userPage, name="user"),
    path('account/', customerAccount, name="account"),
    path('update-account/', updateAccount, name="update_account"),
    path('products/', products, name="products"),
    path('customer_details/<int:pk>/', customerDetails, name="customer_details"),

    path('create_order/', createOrder, name="create_order"),
    path('single_customer_order/<int:pk>/', singleCustomerOrder,
         name="single_customer_order"),
    path('update_order/<int:pk>/', updateOrder, name="update_order"),
    path('delete_order/<int:pk>/', deleteOrder, name="delete_order"),

    path('customers/', customersPage, name="customers"),
    path('create_customer/', createCustomer, name="create_customer"),
    path('update_customer/<int:pk>/', updateCustomer, name="update_customer"),
    path('delete_customer/<int:pk>/', deleteCustomer, name="delete_customer"),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password/password_reset.html"),
         name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_done.html"),
         name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),
         name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_complete.html"),
         name="password_reset_complete"),


]
