from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.filters import SearchFilter, OrderingFilter

from django.db.models import Prefetch, Avg
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    CategoryListSerializer,
    BookListSerializer,
    BookDetailSerializer,
    PublisherDetailSerializer,
    AuthorDetailSerializer,
    ReviewCreateSerializer,
)
from store.models import (
    Category,
    Book,
    Author,
    Publisher,
    Review,
)
from store.filters import BookListFilter


class CategoryListAPIView(ListAPIView):
    """
    This class-based view returns a list of categories,
    where each category may have subcategories up to four levels deep.

    In fact, the nesting of subcategories can be infinite,
    but it is assumed that there will be no more than 4 of them.
    Accordingly, if the nesting is greater,
    then this provokes the "n + 1" problem and may affect performance.
    """
    queryset = Category.objects.filter(parent=None).prefetch_related(
        Prefetch('subcategories', queryset=Category.objects.prefetch_related(
            Prefetch('subcategories', queryset=Category.objects.prefetch_related(
                Prefetch('subcategories', queryset=Category.objects.prefetch_related(
                    Prefetch('subcategories', queryset=Category.objects.prefetch_related(
                        Prefetch('subcategories', queryset=Category.objects.all())
                    ))
                ))
            ))
        ))
    )
    serializer_class = CategoryListSerializer


class BookListAPIView(ListAPIView):
    """
    This endpoint is a class-based view that provides a paginated list of books.
    It retrieves all books from the database and prefetches related authors,
    selecting specific fields for optimization.
    It uses a serializer class to convert the model instances into JSON.
    The endpoint supports filtering, searching,
    and ordering by different criteria such as title, author, publisher, and price.
    """
    queryset = Book.objects.all().prefetch_related(
        Prefetch('author', queryset=Author.objects.all().only('id', 'title')),
    ).only('id', 'title', 'price', 'slug', 'cover_image')
    serializer_class = BookListSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = BookListFilter
    search_fields = (
        'title',
        'author__title',
        'publisher__title',
    )
    ordering_fields = ('price',)


class BookDetailRetrieveAPIView(RetrieveAPIView):
    """
    This endpoint retrieves the details of a single book.
    It optimizes the database queries by selecting related fields from the Publisher, Author, and Review models.
    It calculates the average rating of the book's reviews and selects specific fields for serialization.
    """
    queryset = Book.objects.select_related('category__parent').prefetch_related(
        Prefetch('publisher', queryset=Publisher.objects.all().only('title', 'slug')),
        Prefetch('author', queryset=Author.objects.all().only('title', 'slug')),
        Prefetch('reviews', queryset=Review.objects.select_related('user', 'book').only(
            'id', 'title', 'content', 'rating', 'created',
            'book__id', 'user__first_name', 'user__last_name').all())
    ).annotate(average_rating=Avg('reviews__rating')).filter().only(
        'title', 'category', 'cover_image', 'price', 'slug',
        'publisher', 'author', 'paper', 'language',
        'weight', 'edition', 'amount_pages', 'isbn')
    serializer_class = BookDetailSerializer


class PublisherDetailRetrieveAPIView(RetrieveAPIView):
    """
    This endpoint retrieves detailed information about a single publisher.
    It optimizes database queries by prefetching related books and authors,
    selecting specific fields for serialization.
    """
    queryset = Publisher.objects.all().prefetch_related(
        Prefetch('books', queryset=Book.objects.all().prefetch_related(
            Prefetch('author', queryset=Author.objects.all().only('title'))
        ).only('id', 'title', 'price', 'slug', 'cover_image'))
    )
    serializer_class = PublisherDetailSerializer


class AuthorDetailRetrieveAPIView(RetrieveAPIView):
    """
    This endpoint retrieves detailed information about a single author.
    It optimizes database queries by prefetching related books and authors,
    selecting specific fields for serialization.
    """
    queryset = Author.objects.all().prefetch_related(
        Prefetch('books', queryset=Book.objects.all().prefetch_related(
            Prefetch('author', queryset=Author.objects.all().only('title'))
        ).only('id', 'title', 'price', 'slug', 'cover_image'))
    )
    serializer_class = AuthorDetailSerializer


class ReviewCreateAPIView(CreateAPIView):
    """
    This class-based view is used to handle the creation of new reviews.
    It utilizes the ReviewCreateSerializer for serializing the data provided in the request.
    The IsAuthenticated permission class is applied to ensure that only authenticated users can create reviews.
    """
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]
