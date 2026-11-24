import pytest
from django.urls import reverse
from rest_framework import status

from ads.models import Ad, Comment


@pytest.mark.django_db
class TestAdsEndpointsAndPermissions:
    def test_anonymous_can_list_ads_only(self, api_client, ad):
        list_url = reverse("ads-list")
        detail_url = reverse("ads-detail", kwargs={"pk": ad.pk})

        assert api_client.get(list_url).status_code == status.HTTP_200_OK
        assert api_client.get(detail_url).status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            api_client.post(list_url, {"title": "Test", "price": 100}).status_code
            == status.HTTP_401_UNAUTHORIZED
        )

    def test_pagination_four_items_per_page(self, api_client, user):
        for i in range(6):
            Ad.objects.create(title=f"Товар {i}", price=1000 + i, author=user)

        url = reverse("ads-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 6
        assert len(response.data["results"]) == 4

        page_2 = api_client.get(url, {"page": 2})
        assert len(page_2.data["results"]) == 2

    def test_search_ads_by_title(self, api_client, user):
        Ad.objects.create(title="Mountain Bike Pro", price=20000, author=user)
        Ad.objects.create(title="City Scooter", price=8000, author=user)

        url = reverse("ads-list")
        response = api_client.get(url, {"title": "bike"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["title"] == "Mountain Bike Pro"

    def test_authenticated_user_crud_and_me_endpoint(self, auth_client, user):
        list_url = reverse("ads-list")
        create_resp = auth_client.post(
            list_url,
            {"title": 'Монитор 27"', "price": 25000, "description": "IPS матрица"},
            format="json",
        )
        assert create_resp.status_code == status.HTTP_201_CREATED
        ad_id = create_resp.data["id"]

        detail_url = reverse("ads-detail", kwargs={"pk": ad_id})
        assert auth_client.get(detail_url).status_code == status.HTTP_200_OK

        patch_resp = auth_client.patch(detail_url, {"price": 23000}, format="json")
        assert patch_resp.status_code == status.HTTP_200_OK
        assert patch_resp.data["price"] == 23000

        me_resp = auth_client.get(reverse("ads-me"))
        assert me_resp.status_code == status.HTTP_200_OK
        assert me_resp.data["count"] == 1

        delete_resp = auth_client.delete(detail_url)
        assert delete_resp.status_code == status.HTTP_204_NO_CONTENT

    def test_other_user_cannot_modify_or_delete_ad(self, other_auth_client, ad):
        detail_url = reverse("ads-detail", kwargs={"pk": ad.pk})
        assert (
            other_auth_client.patch(detail_url, {"price": 1}, format="json").status_code
            == status.HTTP_403_FORBIDDEN
        )
        assert (
            other_auth_client.delete(detail_url).status_code
            == status.HTTP_403_FORBIDDEN
        )

    def test_admin_can_modify_and_delete_any_ad(self, admin_client, ad):
        detail_url = reverse("ads-detail", kwargs={"pk": ad.pk})
        patch_resp = admin_client.patch(
            detail_url, {"title": "Изменено админом"}, format="json"
        )
        assert patch_resp.status_code == status.HTTP_200_OK
        assert admin_client.delete(detail_url).status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestCommentsEndpointsAndPermissions:
    def test_anonymous_cannot_access_comments(self, api_client, ad, comment):
        list_url = reverse("ad-comments-list", kwargs={"ad_id": ad.pk})
        assert api_client.get(list_url).status_code == status.HTTP_401_UNAUTHORIZED
        assert (
            api_client.post(list_url, {"text": "Hi"}).status_code
            == status.HTTP_401_UNAUTHORIZED
        )

    def test_user_can_create_and_edit_own_comment(self, auth_client, ad):
        list_url = reverse("ad-comments-list", kwargs={"ad_id": ad.pk})
        create_resp = auth_client.post(list_url, {"text": "Мой отзыв"}, format="json")
        assert create_resp.status_code == status.HTTP_201_CREATED
        comment_id = create_resp.data["id"]

        detail_url = reverse(
            "ad-comments-detail", kwargs={"ad_id": ad.pk, "pk": comment_id}
        )
        assert (
            auth_client.patch(
                detail_url, {"text": "Обновлённый отзыв"}, format="json"
            ).status_code
            == status.HTTP_200_OK
        )
        assert auth_client.delete(detail_url).status_code == status.HTTP_204_NO_CONTENT

    def test_other_user_cannot_modify_or_delete_comment(
        self, other_auth_client, ad, comment
    ):
        detail_url = reverse(
            "ad-comments-detail", kwargs={"ad_id": ad.pk, "pk": comment.pk}
        )
        assert (
            other_auth_client.patch(
                detail_url, {"text": "Чужое"}, format="json"
            ).status_code
            == status.HTTP_403_FORBIDDEN
        )
        assert (
            other_auth_client.delete(detail_url).status_code
            == status.HTTP_403_FORBIDDEN
        )

    def test_admin_can_modify_and_delete_any_comment(self, admin_client, ad, comment):
        detail_url = reverse(
            "ad-comments-detail", kwargs={"ad_id": ad.pk, "pk": comment.pk}
        )
        assert (
            admin_client.patch(
                detail_url, {"text": "Модерация"}, format="json"
            ).status_code
            == status.HTTP_200_OK
        )
        assert admin_client.delete(detail_url).status_code == status.HTTP_204_NO_CONTENT
        assert not Comment.objects.filter(pk=comment.pk).exists()
