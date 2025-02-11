from django.urls import path
from .views import CategoriesView, CategoryDetailView, MenuItemView, MenuItemDetailView, CartView, CartDetailView, OrderView, OrderItemView, OrderItemDetailView,login_page, menu_page, menu_item_page, cart_page, order_page, remove_cart_item
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('categories/', CategoriesView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('api/menu-items/', MenuItemView.as_view(), name='menuitem-list'),
    path('api/menu-items/<int:pk>/', MenuItemDetailView.as_view(), name='menuitem-detail'),
    path('api/cart/', CartView.as_view(), name='cart'),              # ← Changed
    path('api/cart/<int:pk>/', CartDetailView.as_view(), name='cart-detail'),
    path('api/orders/', OrderView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderView.as_view(), name='order-detail'),
    path('order-items/', OrderItemView.as_view(), name='orderitem-list'),
    path('order-items/<int:pk>/', OrderItemDetailView.as_view(), name='orderitem-detail'),
    path('api-token-auth/',obtain_auth_token),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('menu/', menu_page, name='menu'),
    path('menu/<int:pk>/', menu_item_page, name='menu-item'),
    path('cart/', cart_page, name='cart-page'),
    path('orders/', order_page, name='order-page'),
    path('cart/remove/<int:pk>/', remove_cart_item, name='remove-cart-item'),
]