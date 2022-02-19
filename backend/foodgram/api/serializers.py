from rest_framework import serializers

from recipes.models import Amount, Ingredient, Recipe, Tag
from users.serializers import UserSerializer


class IngredientsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = '__all__'

    def get_amount(self, obj):
        amount_object = Amount.objects.get(id=obj.id)
        return amount_object.amount


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class RecipesSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) ###
    ingredients = IngredientsSerializer(many=True)
    tags = TagsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')


class RecipesCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True) ###
    # ingredients = serializers.RelatedField(
    #     queryset=Amount.objects.all(),
    #     many=True,
    #     required=True
    # )
    tags = serializers.RelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')
        read_only_fields = ('is_favorited', 'is_in_shopping_cart')

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
