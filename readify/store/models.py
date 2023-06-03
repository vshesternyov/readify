from slugify import slugify

from django.db import models

from users.models import User


class Category(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Категорія'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name='Батьківська категорія'
    )
    slug = models.SlugField(
        unique=True,
        max_length=255,
        verbose_name='Заповнюється автоматично'
    )

    class Meta:
        verbose_name = 'категорію'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Назва книги'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категорія'
    )
    cover_image = models.ImageField(
        upload_to='book_covers/',
        verbose_name='Фото обкладинки'
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name='Ціна'
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name='Заповнюється автоматично'
    )
    publisher = models.ManyToManyField(
        'Publisher',
        blank=True,
        related_name='books',
        verbose_name='Видавництво'
    )
    author = models.ManyToManyField(
        'Author',
        blank=True,
        related_name='books',
        verbose_name='Автор'
    )
    paper = models.ManyToManyField(
        'Paper',
        blank=True,
        verbose_name='Папір'
    )
    language = models.ManyToManyField(
        'Language',
        blank=True,
        verbose_name='Мова'
    )
    weight = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Вага'
    )
    edition = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Тираж'
    )
    amount_pages = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Кількість сторінок'
    )
    isbn = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='ISBN'
    )

    class Meta:
        verbose_name = 'книгу'
        verbose_name_plural = 'Книжки'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Publisher(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Назва видавництва'
    )
    image = models.ImageField(
        upload_to='publishers/',
        null=True,
        blank=True,
        verbose_name='Фото видавництва'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Опис видавництва'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Заповнюється автоматично'
    )

    class Meta:
        verbose_name = 'видавництво'
        verbose_name_plural = 'Видавництва'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Author(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Ім\'я'
    )
    image = models.ImageField(
        upload_to='authors/',
        null=True,
        blank=True,
        verbose_name='Фото'
    )
    biography = models.TextField(
        null=True,
        blank=True,
        verbose_name='Біографія'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='Заповнюється автоматично'
    )

    class Meta:
        verbose_name = 'автора'
        verbose_name_plural = 'Автори'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Paper(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Папір'
    )

    class Meta:
        verbose_name = 'папір'
        verbose_name_plural = 'Папір'

    def __str__(self):
        return self.title


class Language(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Мова'
    )

    class Meta:
        verbose_name = 'мову'
        verbose_name_plural = 'Мови'

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING = (
        (1, 'Жахливо'),
        (2, 'Погано'),
        (3, 'Типово'),
        (4, 'Чудово'),
        (5, 'Ідеально'),
    )

    book = models.ForeignKey(
        'Book',
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Книга рецензії'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецензії'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )
    content = models.TextField(
        verbose_name='Вміст'
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING,
        verbose_name='Рейтинг'
    )
    created = models.DateField(
        auto_now_add=True,
        verbose_name='Дата створення'
    )

    class Meta:
        verbose_name = 'рецензію'
        verbose_name_plural = 'Рецензії'

    def __str__(self):
        return f'{self.user} : {self.book}'
