from django.db import models
from .utils import generate_random_key


class ApiUser(models.Model):
    host = models.CharField(max_length=140)
    key = models.CharField(max_length=64)
    secret = models.CharField(max_length=64)

    def __str__(self):
        return "{}/{}".format(self.host, self.key)

    @staticmethod
    def create_api_user(host):
        key = generate_random_key(host)
        secret = generate_random_key(host)

        return ApiUser(host=host, key=key, secret=secret)
