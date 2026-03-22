from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Avg, Count

from .models import Category, Product, Review, UserConfirmation
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductWithReviewsSerializer,
    UserRegisterSerializer,
    UserConfirmSerializer
)


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


# USER REGISTER
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


# USER CONFIRM
class UserConfirmView(generics.GenericAPIView):
    serializer_class = UserConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            code = serializer.validated_data["code"]

            try:
                user = User.objects.get(username=username)
                confirmation = UserConfirmation.objects.get(user=user)
            except (User.DoesNotExist, UserConfirmation.DoesNotExist):
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if confirmation.code == code:
                user.is_active = True
                user.save()
                confirmation.delete()

                return Response(
                    {"message": "User confirmed"},
                    status=status.HTTP_200_OK
                )

            return Response(
                {"error": "Invalid code"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)