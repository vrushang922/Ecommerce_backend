from django.test import TestCase
from .models import Order, User, Product
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

""" class UserOrderViewTest(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username = "user1", password = "test")
        user2 = User.objects.create_user(username = "user2", password = "test")
        Order.objects.create(user = user1)
        Order.objects.create(user = user1)
        Order.objects.create(user = user2)
        Order.objects.create(user = user2)

    def test_userorder_endpoint_retrive_only_authenticated_user_orders(self):
        user = User.objects.get(username = "user1")
        self.client.force_login(user)
        response = self.client.get(reverse("user-order"))
        assert response.status_code == status.HTTP_200_OK

        orders = response.json()

        self.assertTrue(all(order["user"] == "user1" for order in orders))
        
    def test_for_unauthenticated_user(self):
        response = self.client.get(reverse("user-order"))
        #assert response.status_code == status.HTTP_403_FORBIDDEN
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  """


class ProductDetailTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username = "admin", password = "admin")
        self.user = User.objects.create_user(username = "user", password = "user")
        self.product = Product.objects.create(name = "pen", price = 10, stock = 12)

        self.url = reverse("product-detail", kwargs = {"product_id": self.product.pk})

    def test_for_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

        response2 = self.client.delete(self.url)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Product.objects.filter(id = self.product.pk).exists())

    def test_for_normal_user(self):
        self.client.login(username = "user", password = "user")
        data = {"name": "update"}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_for_admin_user(self):
        self.client.login(username = "admin", password = "admin")
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id = self.product.pk).exists())







