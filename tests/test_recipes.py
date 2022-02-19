import pytest

from recipes.models import Recipe


class TestUsers:
    url = '/api/recipes/'

    @pytest.mark.django_db(transaction=True)
    def test_recipes_list(self, client, user_client, another_user, recipe,
                          recipe_2, tag, tag_2, ingredient, ingredient_2):
        code_expected = 200
        response = client.get(self.url)
        response_auth = user_client.get(self.url)
        data = response.json()
        data_auth = response_auth.json()
        response_data = data['results']
        response_data_auth = data_auth['results']
        test_recipe = response_data[0]
        print(test_recipe)
        tags_data = [
            {
                'id': tag.id,
                'name': tag.name,
                'color': tag.color,
                'slug': tag.slug
            },
            {
                'id': tag_2.id,
                'name': tag_2.name,
                'color': tag_2.color,
                'slug': tag_2.slug
            }
        ]
        author_data = {
            'email': another_user.email,
            'id': another_user.id,
            'username': another_user.username,
            'first_name': another_user.first_name,
            'last_name': another_user.last_name,
            'is_subscribed': another_user.is_subscribed
        }
        ingredients_data = [
            {
                'id': ingredient.id,
                'name': ingredient.name,
                'amount': ingredient.amount,
                'measurement_unit': ingredient.measurement_unit
            },
            {
                'id': ingredient_2.id,
                'name': ingredient_2.name,
                'amount': ingredient_2.amount,
                'measurement_unit': ingredient_2.measurement_unit
            }
        ]
        data_expected = {
            'id': recipe.id,
            'tags': tags_data,
            'author': author_data,
            'ingredients': ingredients_data,
            'is_favorited': recipe.is_favorited,
            'is_in_shopping_cart': recipe.is_in_shopping_cart,
            'name': recipe.name,
            'image': 'http://testserver/media/https%3A/site.test/image.jpg',
            'text': recipe.text,
            'cooking_time': recipe.cooking_time
        }

        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{self.url}` '
            f'возвращается код {code_expected}'
        )
        assert response_data == response_data_auth, (
            f'Проверьте, что результат GET запроса на `{self.url}` '
            f'от анонима не отличается от результата запроса от '
            f'авторизованного пользователя'
        )
        assert type(data) == dict, (
            f'Проверьте, что при GET запросе на `{self.url}` '
            f'возвращается словарь'
        )
        assert len(response_data) == data['count'] == Recipe.objects.count(), (
            f'Проверьте, что при GET запросе на `{self.url}` '
            f'возвращается весь список пользователей'
        )
        for field in tags_data.items():
            assert field[0] in test_recipe['tags'][0].keys(), (
                f'Проверьте, что добавили поле `{field[0]}` в список полей '
                f'`fields` сериализатора модели Tags, связанного '
                f'с сериализатором модели Recipes'
            )
            assert field[1] == test_recipe['tags'][0][field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` в поле '
                f'`tags` содержит корректные данные'
            )
        for field in data_expected.items():
            assert field[0] in test_recipe.keys(), (
                f'Проверьте, что добавили поле `{field[0]}` в список полей '
                f'`fields` сериализатора модели Recipe'
            )
            assert field[1] == test_recipe[field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` содержит '
                f'корректные данные'
            )
