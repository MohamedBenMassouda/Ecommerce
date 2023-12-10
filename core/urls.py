from django.urls import path, include

urlpatterns = [
    path("users/", include("users.urls"), name="users"),
    path("products/", include("products.urls"), name="products"),
    path("cart/", include("cart.urls"), name="cart"),
]