from django.urls import path

from .views import (
    CategoryListAPIView,
    BookListAPIView,
    BookDetailRetrieveAPIView,
    PublisherDetailRetrieveAPIView,
    AuthorDetailRetrieveAPIView,
    ReviewCreateAPIView
)

urlpatterns = [
    path('category/list/', CategoryListAPIView.as_view(), name='category-list'),
    path('book/list/', BookListAPIView.as_view(), name='book-list'),
    path('book/detail/<int:pk>/', BookDetailRetrieveAPIView.as_view(), name='book-detail'),
    path('publisher/detail/<int:pk>/', PublisherDetailRetrieveAPIView.as_view(), name='publisher-detail'),
    path('author/detail/<int:pk>/', AuthorDetailRetrieveAPIView.as_view(), name='author-detail'),
    path('review/create/', ReviewCreateAPIView.as_view(), name='review-create'),
]
