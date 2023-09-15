from rest_framework import status
from rest_framework.test import APITestCase


class TestAPI(APITestCase):
    url = 'http://127.0.0.1:8000/api/v1/'

    def test_empty_file(self) -> None:
        with open('empty.csv') as file:
            print(file, type(file))
            response = self.client.post(self.url, data={'deals': file}, format='multipart')
            print(response, response.status_code)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_wrong_extension(self) -> None:
        with open('not_csv.txt') as file:
            response = self.client.post(self.url, data={'deals': file}, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_is_file(self) -> None:
        response = self.client.post(self.url, data=None, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
