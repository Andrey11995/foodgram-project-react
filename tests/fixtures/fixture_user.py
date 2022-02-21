import pytest
from rest_framework.test import APIClient


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='TestEmail@mail.ru',
        username='TestUser',
        first_name='TestName',
        last_name='TestLastName',
        password='Password654321'
    )


@pytest.fixture
def user_2(django_user_model):
    return django_user_model.objects.create_user(
        email='TestEmail2@mail.ru',
        username='TestUser2',
        first_name='TestName2',
        last_name='TestLastName2',
        password='Password654321'
    )


@pytest.fixture
def user_3(django_user_model):
    return django_user_model.objects.create_user(
        email='TestEmail3@mail.ru',
        username='TestUser3',
        first_name='TestName3',
        last_name='TestLastName3',
        password='Password654321'
    )


@pytest.fixture
def user_4(django_user_model):
    return django_user_model.objects.create_user(
        email='TestEmail4@mail.ru',
        username='TestUser4',
        first_name='TestName4',
        last_name='TestLastName4',
        password='Password654321'
    )


@pytest.fixture
def user_5(django_user_model):
    return django_user_model.objects.create_user(
        email='TestEmail5@mail.ru',
        username='TestUser5',
        first_name='TestName5',
        last_name='TestLastName5',
        password='Password654321'
    )


@pytest.fixture
def user_6(django_user_model):
    return django_user_model.objects.create_user(
        email='TestEmail6@mail.ru',
        username='TestUser6',
        first_name='TestName6',
        last_name='TestLastName6',
        password='Password654321'
    )


@pytest.fixture
def another_user(django_user_model):
    return django_user_model.objects.create_user(
        email='TestAnotherEmail@mail.ru',
        username='TestAnotherUser',
        first_name='TestAnotherName2',
        last_name='TestAnotherLastName2',
        password='Password654321'
    )


@pytest.fixture
def token(user):
    from rest_framework.authtoken.models import Token
    token = Token.objects.get_or_create(user=user)[0]
    return {
        'auth_token': f'Token {str(token)}',
    }


@pytest.fixture
def user_client(token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=token['auth_token'])
    return client
