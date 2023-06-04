from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from store.models import (
    Author,
    Category,
    Publisher,
    Paper,
    Language,
    Review,
)
from store.utils import get_parent_categories_from_child_to_parent


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('title',)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('title',)


class BookCategorySerializer(ModelSerializer):
    """
    This serializer class is used to serialize a Category model object into JSON format.
    It includes the fields title and a custom field parent_categories.
    The parent_categories field is defined as a SerializerMethodField,
    indicating that its value is derived from a custom method called get_parent_categories.
    This method uses the get_parent_categories_from_child_to_parent function to retrieve the parent categories
    of the current category (obj).
    The parent categories are then serialized using the CategorySerializer
    and returned as the value of the parent_categories field.
    """
    parent_categories = SerializerMethodField()

    class Meta:
        model = Category
        fields = ('title', 'parent_categories')

    @staticmethod
    def get_parent_categories(obj):
        subcategories = get_parent_categories_from_child_to_parent(obj, CategorySerializer)
        return subcategories


class BookPublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('id', 'title', 'slug')


class BookAuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'title', 'slug')


class BookPaperSerializer(ModelSerializer):
    class Meta:
        model = Paper
        fields = ('title',)


class BookLanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = ('title',)


class BookReviewSerializer(ModelSerializer):
    user_first_name = serializers.CharField(source='user.first_name')
    user_last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Review
        fields = ('user', 'user_first_name', 'user_last_name', 'title', 'content', 'rating', 'created')
