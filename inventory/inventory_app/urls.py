from django.urls import path
from .views_auth import ObtainAuthTokenView
from . import views

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),

    # Products
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),

    # Stock movements
    path('stock-movements/', views.StockMovementListCreateView.as_view(), name='stock-movement-list-create'),
    path('stock-movements/<int:pk>/', views.StockMovementRetrieveUpdateDestroyView.as_view(), name='stock-movement-retrieve-update-destroy'),

    path('auth/token/', ObtainAuthTokenView.as_view(), name='token-obtain'),
]
