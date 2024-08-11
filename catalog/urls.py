
from django.contrib import admin
from django.urls import path,include

from catalog import views

urlpatterns = [
    path("",views.home, name='home'),
    #path("dummy/",views.get_dummy,name='dummy'),
    path('signup/',views.user_signup,name="user_signup"),
    path('login/',views.user_login,name="user_login"),
    path('logout/',views.user_logout,name="user_logout"),
    path('product/<int:id>/',views.product_detail,name="product_detail"),
    path('add/to/cart/<int:id>/',views.add_to_cart,name="add_to_cart"),
    path('my/cart/',views.cart_detail,name='cart_detail'),
    path('cart/edit/<int:id>/',views.cart_item_update,name='cart_item_update'),
    path('cart/delete/<int:id>/',views.cart_item_delete,name='cart_item_delete'),
    path('checkout/',views.order_checkout,name='order_checkout'),
    path('payment/<int:id>/',views.make_payment,name='make_payment'),
    path('delivery/address/<int:id>/',views.order_delivery_address,name='order_delivery_address'),
    path('place/order/<int:id>/',views.place_order,name='place_order'),
    path("create/product/", views.create_product,name='create_product'),  
    path("list/product", views.list_product,name='list_product'),
    path("update/product/<int:id>/", views.update_product,name='update_product'),  

    path('api/category/list/',views.CategoryList.as_view(),name='category_list'),
    path('api/category/detail/<int:id>/',views.CategoryDetail.as_view(),name='category_detail'),

    path('dashboard/',views.show_dashboard,name='show_dashboard'),

]