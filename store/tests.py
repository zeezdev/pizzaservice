from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Pizza, Order
from .serializers import OrderSerializer


class OrderTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_pizza = Pizza(name='Pepperoni')
        cls.test_pizza.save()

        # original test data
        cls.data = {
            'pizza': cls.test_pizza.id,
            'customer_name': "Joe",
            'customer_address': "USA, NY",
            'pizza_size': Order.PIZZA_SIZE_30
        }

    @classmethod
    def tearDownClass(cls):
        cls.test_pizza.delete()

    def tearDown(self):
        Order.objects.all().delete()

    def create_test_order_in_db(self, update=None):
        """Create new Order instance in DB"""
        data = self.data.copy()
        if update is not None:
            data.update(update)
        test_order = Order.objects.create(**data)
        return test_order

    def test_create_order(self):
        self.assertEqual(Pizza.objects.get().id, self.test_pizza.id)
        response = self.client.post(reverse('order-list'), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        test_order = Order.objects.get()
        self.assertEqual(test_order.pizza_id, self.test_pizza.id)
        self.assertEqual(test_order.customer_name, self.data['customer_name'])
        self.assertEqual(test_order.customer_address, self.data['customer_address'])
        self.assertEqual(test_order.pizza_size, self.data['pizza_size'])

    def test_get_order(self):
        test_order = self.create_test_order_in_db(update={'pizza': self.test_pizza})

        # fill test info based on test_order
        test_data = self.data.copy()
        test_data['id'] = test_order.id

        response = self.client.get(reverse('order-detail', kwargs={'pk': test_order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, test_data)

    def test_update_order(self):
        test_order = self.create_test_order_in_db(update={'pizza': self.test_pizza})

        test_data = self.data.copy()
        test_data['id'] = test_order.id

        # update order data
        test_data['pizza_size'] = Order.PIZZA_SIZE_50
        response = self.client.patch(reverse('order-detail', kwargs={'pk': test_order.id}), test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check changes in db
        test_order.refresh_from_db()
        self.assertEqual(test_order.pizza_size, test_data['pizza_size'])

    def test_delete_order(self):
        test_order = self.create_test_order_in_db(update={'pizza': self.test_pizza})

        response = self.client.delete(reverse('order-detail', kwargs={'pk': test_order.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=test_order.id).exists())

    def test_get_list_orders(self):
        # Create 3 orders to test
        update = {'pizza': self.test_pizza}
        self.create_test_order_in_db(update=update)
        update['customer_name'] = "Max"
        self.create_test_order_in_db(update=update)
        update['customer_address'] = "Russia, Moscow"
        self.create_test_order_in_db(update=update)

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)

        # fill test info based on test_order
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
