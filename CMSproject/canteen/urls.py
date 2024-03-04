from django.urls import path
from .views import c_canteen_view, s_canteen_view, orders_view, add_menuItem,add_specialItem,delete_specialItem, delete_menuItem,get_order,logout_view, confirm_order

urlpatterns = [
    path('customer/', c_canteen_view, name='c_canteen'),
    path('staff/', s_canteen_view, name='s_canteen'),
    path('order/', orders_view, name='orders'),
    path('staff/addMenuItem', add_menuItem, name='add_menuItem'),
    path('staff/addspecialItem', add_specialItem, name='add_specialItem'),
    path('staff/deletespecialItem', delete_specialItem, name='delete_specialItem'),
    path('staff/deletemenuItem', delete_menuItem, name='delete_menuItem'),
    path('order/get_order', get_order, name='get_the_order'),
    path('order/confirm_order', confirm_order, name='order_confirmed'),
    path('logout/', logout_view, name='logout'),

]