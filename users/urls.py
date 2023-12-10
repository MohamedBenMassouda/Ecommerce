from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.CustomerListView.as_view(), name="customer-list"),
    path("<int:pk>/", views.CustomerView.as_view(), name="customer"),
]
