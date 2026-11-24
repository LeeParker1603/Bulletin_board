import re

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUsersAndAuth:
    def test_user_registration(self, api_client):
        url = reverse("users-list")
        payload = {
            "email": "newuser@example.com",
            "first_name": "Алексей",
            "last_name": "Смирнов",
            "phone": "+79997778899",
            "password": "SuperSecretPassword123!",
        }
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_jwt_token_obtain_and_refresh(self, api_client, user, user_password):
        obtain_url = reverse("token_obtain_pair")
        response = api_client.post(
            obtain_url,
            {"email": user.email, "password": user_password},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

        refresh_url = reverse("token_refresh")
        refresh_resp = api_client.post(
            refresh_url,
            {"refresh": response.data["refresh"]},
            format="json",
        )
        assert refresh_resp.status_code == status.HTTP_200_OK
        assert "access" in refresh_resp.data

    def test_get_current_user_profile(self, auth_client, user):
        url = reverse("users-me")
        response = auth_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
        assert response.data["role"] == "user"

    def test_password_reset_flow(self, api_client, user):
        reset_url = reverse("users-reset-password")
        response = api_client.post(reset_url, {"email": user.email}, format="json")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(mail.outbox) == 1

        email_body = mail.outbox[0].body
        match = re.search(r"password/reset/confirm/([^/]+)/([^/\s]+)", email_body)
        assert match is not None
        uid, token = match.groups()

        confirm_url = reverse("users-reset-password-confirm")
        new_password = "BrandNewPassword789!"
        confirm_resp = api_client.post(
            confirm_url,
            {"uid": uid, "token": token, "new_password": new_password},
            format="json",
        )
        assert confirm_resp.status_code == status.HTTP_204_NO_CONTENT

        user.refresh_from_db()
        assert user.check_password(new_password)

    def test_create_superuser(self, db):
        superuser = User.objects.create_superuser(
            email="super@example.com",
            first_name="Super",
            last_name="Admin",
            password="SuperPassword123!",
        )
        assert superuser.is_superuser
        assert superuser.is_staff
        assert superuser.is_admin
        assert str(superuser) == "super@example.com"
