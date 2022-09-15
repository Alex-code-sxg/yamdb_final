from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Категория произведения')
    slug = models.SlugField(
        unique=True,
        verbose_name='URL')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Жанр произведения')
    slug = models.SlugField(
        unique=True,
        verbose_name='URL')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=160,
        db_index=True,
        verbose_name='Наименование произведения')
    year = models.IntegerField(
        db_index=True,
        verbose_name='Дата создания произведения'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения')
    genre = models.ManyToManyField(
        Genre,
        related_name='title',
        blank=True,
        null=True,
        verbose_name='Жанр произведения')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='title',
        blank=True,
        null=True,
        verbose_name='Категория произведения')

    class Meta:
        ordering = ('year',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, related_name='reviews',
        on_delete=models.CASCADE, blank=True,
        null=True)
    text = models.TextField(
        verbose_name='Текст ревью',
        help_text='Введите ревью'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.text} {self.user.username}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        verbose_name = "Ревью"
        verbose_name_plural = "Ревью"


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Текст комментария',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Напишите комментарий'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.text} {self.user.username}'

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
