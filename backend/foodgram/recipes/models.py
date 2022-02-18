from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название')
    amount = models.FloatField(verbose_name='Количество', null=True)
    measurement_unit = models.CharField(
        max_length=50,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    hex_code = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Идентификатор'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(max_length=150, verbose_name='Название')
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True
    )
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время приготовления'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
