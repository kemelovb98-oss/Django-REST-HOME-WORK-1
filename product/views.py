from rest_framework import generics
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductWithReviewsSerializer
from django.db.models import Avg, Count


# CATEGORY
class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.annotate(
            products_count=Count('product')
        )


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# PRODUCT
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# REVIEW
class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# PRODUCTS WITH REVIEWS + RATING
class ProductReviewsView(generics.ListAPIView):
    serializer_class = ProductWithReviewsSerializer

    def get_queryset(self):
        return Product.objects.annotate(
            rating=Avg('review__stars')
        )