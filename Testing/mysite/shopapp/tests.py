from typing import List, Dict, Any
import random
from string import ascii_letters

from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.urls import reverse

from .models import Order, Product


# Create your tests here.
class OrderDetailTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        permission: Permission = Permission.objects.get(codename="view_order")
        cls.user: User = User.objects.create_user(username="test", password="test")
        cls.user.user_permissions.add(permission)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self):
        self.client.force_login(self.user)
        self.order: Order = Order.objects.create(
            delivery_address="test_address",
            promocode="test_promo",
            user=self.user,
        )

    def tearDown(self):
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse(
                "shopapp:order_details",
                kwargs={"pk": self.order.pk}
            ),
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)

        # Check context
        context_order: Order = response.context["object"]
        self.assertEqual(context_order.pk, self.order.pk)


class OrdersExportWithoutFixturesTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # creating of user with permission
        cls.user_with_per: User = User.objects.create_user(
            username="test_user_with_permission",
            password="test_password"
        )
        cls.user_with_per.is_staff = True
        cls.user_with_per.save()

        # creating list of users for orders and products
        cls.users: List[User] = [
            User.objects.create_user(
                username="".join(random.choices(ascii_letters, k=5)),
                password="".join(random.choices(ascii_letters, k=5)),
            )
            for _ in range(5)
        ]
        cls.users.append(cls.user_with_per)
        # creating list of products
        cls.products: List[Product] = [
            Product.objects.create(
                name="".join(random.choices(ascii_letters, k=5)),
                description="".join(random.choices(ascii_letters, k=10)),
                price=round(random.uniform(1, 100), 2),
                discount=round(random.uniform(1, 100), 2),
                created_by=random.choice(cls.users),
                archived=random.choice((True, False))
            )
            for _ in range(10)
        ]
        # creating list of orders
        cls.orders: List[Order] = [
            Order.objects.create(
                delivery_address="".join(random.choices(ascii_letters, k=10)),
                promocode="".join(random.choices(ascii_letters, k=5)),
                user=random.choice(cls.users),
            )
        ]
        for order in cls.orders:
            order.products.set(random.choices(cls.products, k=random.randint(0, 10)))
            order.save()

        # assemble expected_data
        cls.expected_data: Dict[str, Any] = {
            "orders": [
                {
                    "id": order.pk,
                    "delivery_address": order.delivery_address,
                    "promocode": order.promocode,
                    "user_id": order.user.pk,
                    "products_ids": [
                        product.pk
                        for product in order.products.all()
                    ]
                }
                for order in cls.orders
            ],
        }

    @classmethod
    def tearDownClass(cls):
        for order in cls.orders:
            order.delete()
        for product in cls.products:
            product.delete()
        for user in cls.users:
            user.delete()

    def setUp(self):
        self.client.force_login(self.user_with_per)

    def tearDown(self):
        self.client.logout()

    def test_get_orders_info(self):
        response = self.client.get(reverse("shopapp:export-orders"))
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers["content-type"], "application/json"
        )
        self.assertJSONEqual(response.content, self.expected_data)
