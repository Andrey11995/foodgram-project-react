import pytest

from users.models import User


class TestUsers:
    url = '/api/users/'

    @pytest.mark.django_db(transaction=True)
    def test_users_list(self, client, user_client, user, user_2):
        code_expected = 200
        response = client.get(self.url)
        response_auth = user_client.get(self.url)
        data = response.json()
        data_auth = response_auth.json()
        response_data = data['results']
        response_data_auth = data_auth['results']
        test_user = response_data[0]
        data_expected = {
            'email': user.email,
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_subscribed': user.is_subscribed
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
        assert len(response_data) == data['count'] == User.objects.count(), (
            f'Проверьте, что при GET запросе на `{self.url}` '
            f'возвращается весь список пользователей'
        )
        for field in data_expected.items():
            assert field[0] in test_user.keys(), (
                f'Проверьте, что добавили поле `{field[0]}` в список полей '
                f'`fields` сериализатора модели User'
            )
            assert field[1] == test_user[field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` содержит '
                f'корректные данные'
            )

    @pytest.mark.django_db(transaction=True)
    def test_users_create__empty_request_data(self, client, user):
        users_count = User.objects.count()
        code_expected = 400
        empty_data = {}
        response = client.post(self.url, data=empty_data)
        response_data = response.json()
        required_field = ['Обязательное поле.']
        data_expected = {
            'email': required_field,
            'username': required_field,
            'first_name': required_field,
            'last_name': required_field,
            'password': required_field
        }

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{self.url}` без данных '
            f'возвращается статус {code_expected}'
        )
        assert User.objects.count() == users_count, (
            f'Проверьте, что при POST запросе на `{self.url}` без данных '
            f'не создается новый пользователь'
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
    def test_users_create__invalid_request_data(self, client, user):
        users_count = User.objects.count()
        code_expected = 400
        invalid_data = {
            'email': 'InvalidEmail',
            'username': 'Invalid/Username',
            'first_name': 'invalidName',
            'last_name': 'invalidLastName',
            'password': '12345678'
        }
        response = client.post(self.url, data=invalid_data)
        response_data = response.json()
        data_expected = {
            'email': ['Введите правильный адрес электронной почты.'],
            'username': ['Имя пользователя может содержать латиницу, цифры '
                         'и знаки @ / . / + / - / _'],
            'first_name': ['Имя должно начинаться с заглавной буквы!'],
            'last_name': ['Фамилия должна начинаться с заглавной буквы!'],
            'password': ['Введённый пароль слишком широко распространён.']
        }

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{self.url}` с невалидными '
            f'данными, возвращается статус {code_expected}'
        )
        assert User.objects.count() == users_count, (
            f'Проверьте, что при POST запросе на `{self.url}` с невалидными '
            f'данными не создается новый пользователь'
        )
        for field in data_expected.items():
            assert field[0] in response_data.keys(), (
                f'Убедитесь, что поле `{field[0]}` проверяется на валидность'
            )
            assert field[1] == response_data[field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` после POST '
                f'запроса с невалидными данными: `{field[1]}`'
            )

    @pytest.mark.django_db(transaction=True)
    def test_users_create__existing_username_email(self, client, user):
        users_count = User.objects.count()
        code_expected = 400
        existing_data = {
            'email': user.email,
            'username': user.username,
            'first_name': 'Name',
            'last_name': 'Lastname',
            'password': 'Password654321'
        }
        response = client.post(self.url, data=existing_data)
        response_data = response.json()
        data_expected = {
            'email': ['Пользователь с таким Email уже существует.'],
            'username': ['Пользователь с таким Логин уже существует.']
        }

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{self.url}` с существующими '
            f'данными, возвращается статус {code_expected}'
        )
        assert User.objects.count() == users_count, (
            f'Проверьте, что при POST запросе на `{self.url}` с существующими '
            f'данными не создается новый пользователь'
        )
        for field in data_expected.items():
            assert field[0] in response_data.keys(), (
                f'Убедитесь, что поле `{field[0]}` проверяется на уникальность'
            )
            assert field[1] == response_data[field[0]], (
                f'Убедитесь, что значение поля `{field[0]}` после POST '
                f'запроса с существующими данными: `{field[1]}`'
            )

    @pytest.mark.django_db(transaction=True)
    def test_users_create__valid_request_data(self, client, user):
        users_count = User.objects.count()
        code_expected = 201
        valid_data = {
            'email': 'Valid@Email.ru',
            'username': 'ValidUsername',
            'first_name': 'Validname',
            'last_name': 'Validlastname',
            'password': 'Password654321'
        }
        response = client.post(self.url, data=valid_data)
        response_data = response.json()
        data_expected = {
            'email': 'Valid@Email.ru',
            'id': response_data['id'],
            'username': 'ValidUsername',
            'first_name': 'Validname',
            'last_name': 'Validlastname'
        }

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{self.url}` с валидными '
            f'данными, возвращается статус {code_expected}'
        )
        assert User.objects.count() == users_count + 1, (
            f'Проверьте, что при POST запросе на `{self.url}` с валидными '
            f'данными создается новый пользователь'
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

    @pytest.mark.django_db(transaction=True)
    def test_users_detail__not_auth(self, client, user):
        url = self.url + str(user.id) + '/'
        code_expected = 401
        data_expected = {'detail': 'Учетные данные не были предоставлены.'}
        response = client.get(url)
        response_data = response.json()

        assert response.status_code == code_expected, (
            f'Проверьте, что при GET запросе на `{url}` '
            f'от неавторизованного пользователя, возвращается статус '
            f'{code_expected}'
        )
        assert response_data == data_expected, (
            f'Проверьте, что при GET запросе на `{url}` '
            f'от неавторизованного пользователя, возвращается сообщение: '
            f'{data_expected["detail"]}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_detail__not_found(self, user_client, user):
        url = self.url + '404/'
        code_expected = 404
        data_expected = {'detail': 'Страница не найдена.'}
        response = user_client.get(url)
        response_data = response.json()

        assert response.status_code == code_expected, (
            f'Проверьте, что при GET запросе на `{url}` '
            f'на несуществующего пользователя, возвращается статус '
            f'{code_expected}'
        )
        assert response_data == data_expected, (
            f'Проверьте, что при GET запросе на `{url}` '
            f'на несуществующего пользователя, возвращается сообщение: '
            f'{data_expected["detail"]}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_detail_me__auth_user(self, user_client, user):
        urls = [
            self.url + str(user.id) + '/',
            self.url + 'me/'
        ]
        code_expected = 200
        data_expected = {
            'email': user.email,
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_subscribed': user.is_subscribed
        }
        for url in urls:
            response = user_client.get(url)
            response_data = response.json()

            assert response.status_code == code_expected, (
                f'Проверьте, что при GET запросе на `{url}` '
                f'от авторизованного пользователя, возвращается статус '
                f'{code_expected}'
            )
            for field in data_expected.items():
                assert field[0] in response_data.keys(), (
                    f'Убедитесь, что добавили поле `{field[0]}` в список '
                    f'полей `fields` сериализатора модели User'
                )
                assert field[1] == response_data[field[0]], (
                    f'Убедитесь, что значение поля `{field[0]}` содержит '
                    f'корректные данные'
                )

    @pytest.mark.django_db(transaction=True)
    def test_users_me__not_auth(self, client, user):
        url = self.url + 'me/'
        code_expected = 401
        data_expected = {'detail': 'Учетные данные не были предоставлены.'}
        response = client.get(url)
        response_data = response.json()

        assert response.status_code == code_expected, (
            f'Проверьте, что при GET запросе на `{url}` '
            f'от неавторизованного пользователя, возвращается статус '
            f'{code_expected}'
        )
        assert response_data == data_expected, (
            f'Проверьте, что при GET запросе на `{url}` '
            f'от неавторизованного пользователя возвращается сообщение: '
            f'{data_expected["detail"]}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_set_password__not_auth(self, client):
        url = self.url + 'set_password/'
        code_expected = 401
        data_expected = {'detail': 'Учетные данные не были предоставлены.'}
        response = client.get(url)
        response_data = response.json()

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{url}` '
            f'от неавторизованного пользователя, возвращается статус '
            f'{code_expected}'
        )
        assert response_data == data_expected, (
            f'Проверьте, что при POST запросе на `{url}` '
            f'от неавторизованного пользователя возвращается сообщение: '
            f'{data_expected["detail"]}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_set_password__invalid_data(self, user_client):
        url = self.url + 'set_password/'
        code_expected = 400
        invalid_data = {
            'new_password': 'password',
            'current_password': 'InvalidPassword'
        }
        data_expected = {'current_password': ['Неправильный пароль.']}
        response = user_client.post(url, data=invalid_data)
        response_data = response.json()

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{url}` '
            f'с невалидными паролями, возвращается статус '
            f'{code_expected}'
        )
        assert response_data == data_expected, (
            f'Проверьте, что при POST запросе на `{url}` '
            f'с невалидными паролями возвращается сообщение: '
            f'{data_expected["current_password"]}'
        )

        invalid_data = {
            'new_password': 'password',
            'current_password': 'Password654321'
        }
        data_expected = {
            'new_password': ['Введённый пароль слишком широко распространён.']
        }
        response = user_client.post(url, data=invalid_data)
        response_data = response.json()

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{url}` '
            f'с невалидным новым и верным старым паролем, '
            f'возвращается статус {code_expected}'
        )
        assert response_data == data_expected, (
            f'Проверьте, что при POST запросе на `{url}` '
            f'с невалидным новым и верным старым паролем, '
            f'возвращается сообщение: {data_expected["new_password"]}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_users_set_password__valid_data(self, client, user_client, user):
        url = self.url + 'set_password/'
        code_expected = 204
        valid_data = {
            'new_password': 'NewPassword654321',
            'current_password': 'Password654321'
        }
        response = user_client.post(url, data=valid_data)

        assert response.status_code == code_expected, (
            f'Проверьте, что при POST запросе на `{url}` '
            f'с валидными данными, возвращается статус '
            f'{code_expected}'
        )

        url_login = '/api/auth/token/login/'
        code_expected = 200
        data = {
            'email': user.email,
            'password': valid_data['new_password']
        }
        field_expected = 'auth_token'
        response = client.post(url_login, data=data)
        response_data = response.json()

        assert response.status_code == code_expected, (
            f'Убедитесь, что при запросе `{url_login}` с новым паролем, '
            f'возвращается код {code_expected}'
        )
        assert field_expected in response_data.keys(), (
            f'Убедитесь, что при запросе `{url_login}` с новым паролем, '
            f' в ответе возвращается ключ {field_expected}, '
            f'где содержится токен'
        )
