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
    
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer
from rest_framework import generics


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserConfirmation
from .serializers import UserConfirmSerializer


class UserConfirmView(APIView):

    def post(self, request):
        serializer = UserConfirmSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            code = serializer.validated_data["code"]

            try:
                user = User.objects.get(username=username)
                confirmation = UserConfirmation.objects.get(user=user)
            except:
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