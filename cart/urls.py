from django.urls import path

from . import views

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
    path("items/<int:item_id>/", views.CartItemView.as_view(), name='cart_item'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('remove/', views.remove_from_cart, name='remove_from_cart'),
]