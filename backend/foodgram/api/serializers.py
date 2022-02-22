import base64
import imghdr
import uuid

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Amount, Ingredient, Recipe, Tag
from users.serializers import UserSerializer


class IngredientsViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientsForRecipeSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('name', 'measurement_unit')

    def get_amount(self, obj):
        amount_object = get_object_or_404(Amount, ingredient=obj.id)
        return amount_object.amount


class AmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient'
    )
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = Amount
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_name(self, amount):
        ing_id = amount.ingredient.id
        ing = get_object_or_404(Ingredient, id=ing_id)
        return ing.name

    def get_measurement_unit(self, amount):
        ing_id = amount.ingredient.id
        ing = get_object_or_404(Ingredient, id=ing_id)
        return ing.measurement_unit


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('name', 'color', 'slug')


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


class RecipesSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) ###
    ingredients = IngredientsForRecipeSerializer(many=True)
    tags = TagsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')


class TagListField(serializers.RelatedField):

    def to_representation(self, value):
        data = {
            'id': value.id,
            'name': value.name,
            'color': value.color,
            'slug': value.slug
        }
        return data

    def to_internal_value(self, data):
        return data


class RecipesCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) ###
    ingredients = AmountSerializer(many=True)
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
        tags_list = [get_object_or_404(Tag, id=tag) for tag in tags]
        recipe.ingredients.set(amounts)
        recipe.tags.set(tags_list)
        return recipe

    def update(self, instance, validated_data):
        pass

    def validate_name(self, name):
        if not name.istitle():
            raise serializers.ValidationError(
                'Название должно начинаться с заглавной буквы!'
            )
        elif len(name) < 3:
            raise serializers.ValidationError(
                'Название должно содержать от 3 символов!'
            )
        return name

    def validate_text(self, text):
        if len(text) < 10:
            raise serializers.ValidationError(
                'Описание должно содержать от 10 символов!'
            )
        return text
