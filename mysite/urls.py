from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.login_request, name="login"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    path('register/', views.register, name="register"),
    path('home/', views.index, name='index'),
    path('orders/', views.order_summary, name='orders'),
    path('contact/', views.contact, name='contact'),
    path('order/', views.order, name='order'),
    path('products/bread/', views.bread, name='bread'),
    path('products/cakes/', views.cake, name='cakes'),
    path('products/cupcakes/', views.cupcakes, name='cupcakes'),
    path('products/swissroll/', views.swissrolls, name='swissrolls'),
    path('products/donuts/', views.donuts, name='donuts'),
    path('products/others/', views.others, name='others'),
    path('products/bread/add_to_cart/<int:product_id>/', views.add_to_cart, 
         name='add_to_cart'),
    path('product/<int:pk>/', views.add_to_cart, name='product'),
    path('products/bread/add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_item_from_cart/<int:item_id>/', views.remove_from_cart,
         name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
