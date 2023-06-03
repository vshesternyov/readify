from django.contrib import admin

from .models import (
    Category,
    Book,
    Publisher,
    Author,
    Paper,
    Language,
    Review
)

admin.site.register(Paper)
admin.site.register(Language)
admin.site.register(Review)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}
