from django.urls import path
from .views import UserRegisterView
from .views import UserConfirmView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CategoryListView,
    CategoryDetailView,
    ProductListView,
    ProductDetailView,
    ReviewListView,
    ReviewDetailView,
    ProductReviewsView,
)

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('categories/<int:pk>/', CategoryDetailView.as_view()),

    path('products/', ProductListView.as_view()),
    path('products/<int:pk>/', ProductDetailView.as_view()),

    path('reviews/', ReviewListView.as_view()),
    path('reviews/<int:pk>/', ReviewDetailView.as_view()),
    path('products/reviews/', ProductReviewsView.as_view()),
    path('users/register/', UserRegisterView.as_view()),
    path('users/confirm/', UserConfirmView.as_view()),
    path('users/login/', TokenObtainPairView.as_view()),
    path('users/refresh/', TokenRefreshView.as_view()),
]

