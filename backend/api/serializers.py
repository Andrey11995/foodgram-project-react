import base64
import imghdr
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from recipes.models import (Amount, Favorite, Ingredient, Recipe, ShoppingCart,
                            Tag)
from rest_framework import serializers
from users.serializers import UserSerializer


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            self.fail('invalid_image')
        name = str(uuid.uuid4())[:10]
        extension = imghdr.what(name, decoded_file)
        extension = 'jpg' if extension == 'jpeg' else extension
        file_name = f'{name}.{extension}'
        data = ContentFile(decoded_file, name=file_name)
        return super(Base64ImageField, self).to_internal_value(data)


class TagListField(serializers.RelatedField):

    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
            'color': value.color,
            'slug': value.slug
        }

    def to_internal_value(self, data):
        try:
            return Tag.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                'Недопустимый первичный ключ "404" - объект не существует.'
            )


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientsAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    name = serializers.SerializerMethodField(read_only=True)
    measurement_unit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def _get_ingredient(self, ingredient_id):
        return get_object_or_404(Ingredient, id=ingredient_id)

    def get_name(self, amount):
        return self._get_ingredient(amount.ingredient.id).name

    def get_measurement_unit(self, amount):
        return self._get_ingredient(amount.ingredient.id).measurement_unit


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug')


class RecipesSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientsAmountSerializer(many=True)
    tags = TagsSerializer(many=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(
                user=user,
                recipe=recipe
            ).exists()
        return False

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
            ).exists()
        return False


class RecipesCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientsAmountSerializer(many=True)
    tags = TagListField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('is_favorited', 'is_in_shopping_cart')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        amounts = []
        for ingredient in ingredients:
            amount, status = Amount.objects.get_or_create(**ingredient)
            amounts.append(amount)
        recipe.ingredients.set(amounts)
        recipe.tags.set(tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.save()
        amounts = []
        for ingredient in ingredients:
            amount = get_object_or_404(Amount, **ingredient)
            amounts.append(amount)
        instance.ingredients.set(amounts)
        instance.tags.set(tags)
        return instance

    def validate_name(self, name):
        if not name.split(' ')[0].istitle():
            raise serializers.ValidationError(
                'Название должно начинаться с заглавной буквы!'
            )
        elif len(name) < 3:
            raise serializers.ValidationError(
                'Название должно содержать от 3 символов!'
            )
        return name

    def validate_text(self, text):
        if not text.split(' ')[0].istitle():
            raise serializers.ValidationError(
                'Описание должно начинаться с заглавной буквы!'
            )
        elif len(text) < 10:
            raise serializers.ValidationError(
                'Описание должно содержать от 10 символов!'
            )
        return text