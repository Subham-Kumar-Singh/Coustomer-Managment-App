from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('product/',views.products,name="product"),
    path('customer/<str:pk_test>/',views.customer,name="customer"),
    path('order_form/<str:pk>/',views.orderform,name="order_form"),
    path('update_order/<str:pk>/',views.updateOrder,name="update_order"),
    path('delete_order/<str:pk>/',views.deleteOrder,name="delete_order"),

    path('user/',views.UserPage,name="userPage"),
    path('login/',views.loginPage,name="login"),
    path('register/',views.register,name="register"),
    path('logout/',views.logOutUser,name="logout"),
    path('account/',views.accountSettings,name="account"),
]