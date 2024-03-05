from django.urls import path
from .views import c_canteen_view, s_canteen_view, orders_view, add_menuItem,add_specialItem,delete_specialItem, delete_menuItem,get_order, confirm_order,get_notifications,mark_notifications_as_seen,reject_order,completed_order,sales_view

urlpatterns = [
    path('customer/', c_canteen_view, name='c_canteen'),
    path('staff/', s_canteen_view, name='s_canteen'),
    path('order/', orders_view, name='orders'),
    path('sales/', sales_view, name='sales'),
    path('staff/addMenuItem', add_menuItem, name='add_menuItem'),
    path('staff/addspecialItem', add_specialItem, name='add_specialItem'),
    path('staff/deletespecialItem', delete_specialItem, name='delete_specialItem'),
    path('staff/deletemenuItem', delete_menuItem, name='delete_menuItem'),
    path('order/get_order', get_order, name='get_the_order'),
    path('order/confirm_order', confirm_order, name='order_confirmed'),
    path('order/reject_order', reject_order, name='order_rejected'),
    path('order/completed_order', completed_order, name='order_completed'),
    path('api/get_notifications/', get_notifications, name='get_notifications'),
    path('mark_notifications_as_seen/', mark_notifications_as_seen, name='mark_notifications_as_seen'),

]