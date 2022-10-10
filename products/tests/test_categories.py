from rest_framework.test import APIClient
from rest_framework import status

class TestCreateCategory:
    def test_if_user_is_anonymous_return_401(self):
        client = APIClient()
        response = client.post('/product/categories/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED