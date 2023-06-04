from rest_framework.fields import SerializerMethodField, FloatField
from rest_framework.serializers import ModelSerializer

from store.api.nested_serializers import (
    AuthorSerializer,
    BookCategorySerializer,
    BookPublisherSerializer,
    BookAuthorSerializer,
    BookPaperSerializer,
    BookLanguageSerializer,
    BookReviewSerializer,
)
from store.models import (
    Category,
    Book,
    Publisher,
    Author,
    Review,
)


class CategoryListSerializer(ModelSerializer):
    """
    This serializer class is used to serialize a Category model object into JSON format.
    It includes the fields id, title, slug, and a custom field subcategories.
    The subcategories field is defined as a SerializerMethodField,
    which means its value is derived from a custom method called get_subcategories.
    This method retrieves the related subcategories of the category
    and serializes them using the same serializer class (CategoryListSerializer) recursively.
    The serialized subcategories are then returned as the value of the subcategories field.
    The Meta class within the serializer specifies the model (Category)
    and the fields to be included in the serialized output.
    Overall, this serializer provides a representation of a category
    and its related subcategories in a nested structure.
    """
    subcategories = SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'slug', 'subcategories')

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        serializer = self.__class__(subcategories, many=True)
        return serializer.data


class BookListSerializer(ModelSerializer):
    author = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'price', 'slug', 'cover_image', 'author')


class BookDetailSerializer(ModelSerializer):
    category = BookCategorySerializer(many=False)
    publisher = BookPublisherSerializer(many=True)
    author = BookAuthorSerializer(many=True)
    paper = BookPaperSerializer(many=True)
    language = BookLanguageSerializer(many=True)
    reviews = BookReviewSerializer(many=True)
    average_rating = FloatField()

    class Meta:
        model = Book
        fields = (
            'title', 'category', 'cover_image', 'price', 'slug',
            'publisher', 'author', 'paper', 'language',
            'weight', 'edition', 'amount_pages', 'isbn', 'reviews', 'average_rating'
        )


class PublisherDetailSerializer(ModelSerializer):
    books = BookListSerializer(many=True)

    class Meta:
        model = Publisher
        fields = ('id', 'title', 'image', 'description', 'slug', 'books')


class AuthorDetailSerializer(ModelSerializer):
    books = BookListSerializer(many=True)

    class Meta:
        model = Author
        fields = ('id', 'title', 'image', 'biography', 'slug', 'books')


class ReviewCreateSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('book', 'user', 'title', 'content', 'rating')
