from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name="index"),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('logout/',views.logout,name='logout'),
    path('cart/', views.cart, name='cart'),
    path('details/',views.fillDetails,name='details'),
    path('checkout/',views.checkOut,name='checkout'),
    path('orders/',views.orders,name='order')
]