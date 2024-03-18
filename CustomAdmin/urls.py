
from django.urls import path
from . import views
from .views import update_order_status

# app_name = 'custom_admin'
urlpatterns = [
    path('register_admin/', views.register_custom_admin, name='register_admin'),
    path('admin_login/', views.custom_admin_login, name='admin_login'),
    path('custom_admin/orders/', views.order_list, name='order_list'),
    path('update_order_status/<int:order_id>/', views.update_order_status,
         name='update_order_status'),
    path('logout/', views.admin_logout_request, name="logout"),
]