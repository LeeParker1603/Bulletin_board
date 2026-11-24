import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from ads.models import Ad, Comment
from users.models import UserRole

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_password():
    return "StrongTestPass123!"


@pytest.fixture
def user(db, user_password):
    return User.objects.create_user(
        email="user1@example.com",
        first_name="Иван",
        last_name="Петров",
        phone="+79991112233",
        password=user_password,
        role=UserRole.USER,
    )


@pytest.fixture
def other_user(db, user_password):
    return User.objects.create_user(
        email="user2@example.com",
        first_name="Мария",
        last_name="Сидорова",
        phone="+79994445566",
        password=user_password,
        role=UserRole.USER,
    )


@pytest.fixture
def admin_user(db, user_password):
    return User.objects.create_user(
        email="admin@example.com",
        first_name="Админ",
        last_name="Главный",
        phone="+79990000000",
        password=user_password,
        role=UserRole.ADMIN,
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def other_auth_client(other_user):
    client = APIClient()
    client.force_authenticate(user=other_user)
    return client


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def ad(db, user):
    return Ad.objects.create(
        title="Ноутбук Lenovo ThinkPad",
        price=55000,
        description="Рабочий ноутбук в отличном состоянии",
        author=user,
    )


@pytest.fixture
def comment(db, user, ad):
    return Comment.objects.create(
        text="Отличный товар, всё соответствует описанию",
        author=user,
        ad=ad,
    )
