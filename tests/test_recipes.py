import pytest

from django.core.files.uploadedfile import SimpleUploadedFile

from recipes.models import Recipe


class TestUsers:
    url = '/api/recipes/'
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    test_image = SimpleUploadedFile('small.gif', small_gif,
                                    content_type='image/gif')

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
        for field in tags_data[0].items():
            assert field[0] in test_recipe['tags'][0].keys(), (
                f'Проверьте, что добавили поле `{field[0]}` в список полей '
                f'`fields` сериализатора модели Tag, связанного '
                f'с сериализатором модели Recipes'
            )
            assert field[1] == test_recipe['tags'][0][field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` в поле '
                f'`tags` содержит корректные данные'
            )
        for field in ingredients_data[0].items():
            assert field[0] in test_recipe['ingredients'][0].keys(), (
                f'Проверьте, что добавили поле `{field[0]}` в список полей '
                f'`fields` сериализатора модели Ingredient, связанного '
                f'с сериализатором модели Recipes'
            )
            assert field[1] == test_recipe['ingredients'][0][field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` в поле '
                f'`ingredients` содержит корректные данные'
            )
        for field in author_data.items():
            assert field[0] in test_recipe['author'].keys(), (
                f'Проверьте, что добавили поле `{field[0]}` в список полей '
                f'`fields` сериализатора модели User, связанного '
                f'с сериализатором модели Recipes'
            )
            assert field[1] == test_recipe['author'][field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` в поле '
                f'`author` содержит корректные данные'
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

    @pytest.mark.django_db(transaction=True)
    def test_recipes_detail__not_found(self, client, user):
        url = self.url + '404/'
        code_expected = 404
        data_expected = {'detail': 'Страница не найдена.'}
        response = client.get(url)
        response_data = response.json()

        assert response.status_code == code_expected, (
            f'Проверьте, что при GET запросе на `{url}` '
            f'на несуществующий рецепт, возвращается код '
            f'{code_expected}'
        )
        assert response_data == data_expected, (
            f'Проверьте, что при GET запросе на `{url}` '
            f'на несуществующий рецепт, возвращается сообщение: '
            f'{data_expected["detail"]}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipes_detail(self, client, user_client, user, recipe_2, tag,
                            ingredient):
        url = self.url + str(recipe_2.id) + '/'
        code_expected = 200
        response = client.get(url)
        response_auth = user_client.get(url)
        response_data = response.json()
        response_data_auth = response_auth.json()
        tags_data = [
            {
                'id': tag.id,
                'name': tag.name,
                'color': tag.color,
                'slug': tag.slug
            }
        ]
        author_data = {
            'email': user.email,
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_subscribed': user.is_subscribed
        }
        ingredients_data = [
            {
                'id': ingredient.id,
                'name': ingredient.name,
                'amount': ingredient.amount,
                'measurement_unit': ingredient.measurement_unit
            }
        ]
        data_expected = {
            'id': recipe_2.id,
            'tags': tags_data,
            'author': author_data,
            'ingredients': ingredients_data,
            'is_favorited': recipe_2.is_favorited,
            'is_in_shopping_cart': recipe_2.is_in_shopping_cart,
            'name': recipe_2.name,
            'image': 'http://testserver/media/https%3A/site.test/image2.jpg',
            'text': recipe_2.text,
            'cooking_time': recipe_2.cooking_time
        }

        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url}` '
            f'возвращается код {code_expected}'
        )
        assert response_data == response_data_auth, (
            f'Проверьте, что результат GET запроса на `{url}` '
            f'от анонима не отличается от результата запроса от '
            f'авторизованного пользователя'
        )
        for field in data_expected.items():
            assert field[0] in response_data.keys(), (
                f'Проверьте, что добавили поле `{field[0]}` в список полей '
                f'`fields` сериализатора модели Recipe'
            )
            assert field[1] == response_data[field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` содержит '
                f'корректные данные'
            )

    @pytest.mark.django_db(transaction=True)
    def test_recipes_create__not_auth(self, client, tag, ingredient):
        recipes_count = Recipe.objects.count()
        code_expected = 401
        ingredients_data = [
            {
                'id': ingredient.id,
                'amount': 2.5
            }
        ]
        data = {
            'ingredients': ingredients_data,
            'tags': [tag.id],
            'image': self.test_image,
            'name': 'Рецепт',
            'text': 'Описание рецепта',
            'cooking_time': 1
        }
        data_expected = {'detail': 'Учетные данные не были предоставлены.'}
        response = client.post(self.url, data=data)
        response_data = response.json()

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{self.url}` '
            f'от неавторизованного пользователя, возвращается статус '
            f'{code_expected}'
        )
        assert Recipe.objects.count() == recipes_count, (
            f'Проверьте, что при POST запросе на `{self.url}` '
            f'от неавторизованного пользователя, не создается новый рецепт'
        )
        assert response_data == data_expected, (
            f'Проверьте, что при POST запросе на `{self.url}` '
            f'от неавторизованного пользователя, возвращается сообщение: '
            f'{data_expected["detail"]}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_recipes_create__empty_request_data(self, user_client):
        recipes_count = Recipe.objects.count()
        code_expected = 400
        empty_data = {}
        response = user_client.post(self.url, data=empty_data)
        response_data = response.json()
        required_field = ['Обязательное поле.']
        data_expected = {
            'ingredients': required_field,
            'tags': required_field,
            'image': ['Ни одного файла не было отправлено.'],
            'name': required_field,
            'text': required_field,
            'cooking_time': required_field
        }

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{self.url}` без данных '
            f'возвращается статус {code_expected}'
        )
        assert Recipe.objects.count() == recipes_count, (
            f'Проверьте, что при POST запросе на `{self.url}` без данных '
            f'не создается новый рецепт'
        )
        for field in data_expected.items():
            assert field[0] in response_data.keys(), (
                f'Проверьте, что поле `{field[0]}` является обязательным'
            )
            assert field[1] == response_data[field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` после POST '
                f'запроса без данных: `{field[1]}`'
            )

    @pytest.mark.django_db(transaction=True)
    def test_recipes_create__invalid_request_data(self, user_client):
        recipes_count = Recipe.objects.count()
        code_expected = 400
        invalid_ingredients_data = [
            {
                'id': 404,
                'amount': 0
            }
        ]
        invalid_data = {
            'ingredients': invalid_ingredients_data,
            'tags': [404],
            'image': 'invalid_link',
            'name': 'рецепт',
            'text': 'описание',
            'cooking_time': 0
        }
        response = user_client.post(self.url, data=invalid_data)
        response_data = response.json()
        data_expected = {
            'ingredients': ['Обязательное поле.'],
            'tags': ['Обязательное поле.'],
            'image': ['Загруженный файл не является корректным файлом.'],
            'name': ['Название должно начинаться с заглавной буквы!'],
            'text': ['Описание должно содержать от 10 символов!'],
            'cooking_time': ['Убедитесь, что это значение больше либо '
                             'равно 1.']
        }

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{self.url}` с невалидными '
            f'данными, возвращается статус {code_expected}'
        )
        assert Recipe.objects.count() == recipes_count, (
            f'Проверьте, что при POST запросе на `{self.url}` с невалидными '
            f'данными не создается новый рецепт'
        )
        for field in data_expected.items():
            assert field[0] in response_data.keys(), (
                f'Убедитесь, что поле `{field[0]}` проверяется на валидность'
            )
            assert field[1] == response_data[field[0]], (
                f'Убедитесь, что поле `{field[0]}` после POST запроса '
                f'с невалидными данными выдает соответствующую ошибку'
            )

    @pytest.mark.django_db(transaction=True)
    def test_recipes_create__valid_request_data(self, user_client, another_user, tag, tag_2, ingredient, ingredient_2):
        recipes_count = Recipe.objects.count()
        code_expected = 201
        valid_ingredients_data = [
            {
                'id': ingredient.id,
                'amount': 2.5
            },
            {
                'id': ingredient_2.id,
                'amount': 10
            }
        ]
        valid_data = {
            'ingredients': valid_ingredients_data,
            'tags': [tag.id, tag_2.id],
            'image': self.test_image,
            'name': 'Рецепт',
            'text': 'Описание рецепта',
            'cooking_time': 30
        }
        response = user_client.post(self.url, data=valid_data)
        response_data = response.json()
        print(response_data)
        data_expected = {
            'id': 1,
            'tags': [tag.id, tag_2.id],
            'author': '',
            'ingredients': valid_ingredients_data,
            'is_favorited': False,
            'is_in_shopping_cart': False,
            'name': 'Рецепт',
            'image': 'test_image.jpg',
            'text': 'Описание рецепта',
            'cooking_time': 30
        }

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{self.url}` с валидными '
            f'данными, возвращается статус {code_expected}'
        )
        assert Recipe.objects.count() == recipes_count + 1, (
            f'Проверьте, что при POST запросе на `{self.url}` с валидными '
            f'данными создается новый рецепт'
        )
        for field in data_expected.items():
            assert field[0] in response_data.keys(), (
                f'Убедитесь, что поле `{field[0]}` присутствует в выдаче '
                f'после успешного создания пользователя'
            )
            assert field[1] == response_data[field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` содержит '
                f'корректные данные'
            )
