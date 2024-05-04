from django.test import Client, SimpleTestCase
from django.urls import reverse
import uuid


class APITests(SimpleTestCase):
    def setUp(self):
        self.client = Client()

    def test_echo(self):
        response = self.client.get(reverse('echo'), {'string': 'Hello World!'})
        self.assertEqual(response.content, b'Hello World!')

    def test_get_price(self):
        data = {
            'itemId': '73eebcb6-a5d8-46ff-8a5e-0b9e79be1489',
            'quantity': 2
        }
        response = self.client.post(reverse('get_price'), data, content_type='application/json')
        response_data = response.json()
        self.assertEqual(response_data['itemId'], data['itemId'])
        self.assertEqual(response_data['quantity'], data['quantity'])
        self.assertEqual(response_data['perItemPrice'], 250)
        self.assertEqual(response_data['totalPricePreTax'], 500)
        self.assertEqual(response_data['taxRate'], 0.2)
        self.assertEqual(response_data['totalPriceWithTax'], 600)

    def test_compute(self):
        data = [9, 58, 79, 99, 33, 67, 68, 48, 26, 42, 11,
                37, 49, 35, 28, 55, 19, 72, 61, 1, 19, 31, 92, 84, 21,
                99, 25, 29, 42, 61, 64, 84, 99, 40, 85, 39, 11, 13, 29, 49,
                95, 29, 30, 21, 12, 52, 98, 51, 18, 76, 5, 54, 16, 28, 83,
                59, 59, 36, 63, 22, 63, 15, 41, 24, 84, 62, 86, 23, 95, 63,
                99, 46, 40, 57, 97, 6, 82, 96, 88, 66, 60, 99, 92, 75, 58,
                32, 15, 32, 72, 61, 52, 50, 61, 81, 65, 46, 40, 71, 32, 71]
        response = self.client.post(reverse('compute'), data, content_type='application/json')
        self.assertEqual(response.content, b'f79f064b519bfb1197b5c0f2e0c03c54e52fada9b850d681f7dd305f047ea1bb')

    def test_parse(self):
        data = []
        for i in range(100):
            data.append(uuid.uuid4().hex)

        random_index = uuid.uuid4().int % 100
        search_string = data[random_index]

        response = self.client.post(reverse('parse') + f'?searchString={search_string}', data, content_type='application/json')
        self.assertEqual(response.content, str(random_index).encode())

    def test_query(self):
        response = self.client.get(reverse('query') + '?initialPrimaryKey=038aca33-a8c0-4b5d-8543-cc50b8f4895c')
        self.assertEqual(response.content, b'200')
