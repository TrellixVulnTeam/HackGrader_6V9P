from test_plus import TestCase

from django.contrib.auth.models import User

from hacktester.api_auth.models import ApiUser


class TestAdminApiUserCreation(TestCase):
    def setUp(self):
        self.test_password = 'testpassword'
        self.user = User.objects.create_superuser(username="admin",
                                                  email="admin@admin.com",
                                                  password=self.test_password)
        self.url = self.reverse('admin:api_auth_apiuser_add')

    def test_api_user_is_created_correctly_on_post_to_admin_creation_page(self):
        api_user_count = ApiUser.objects.count()
        with self.login(username=self.user.username, password=self.test_password):
            data = {'host': 'exampleurl.com'}
            response = self.post(self.url, data=data)
            self.response_302(response)
            self.assertEqual(api_user_count + 1, ApiUser.objects.count())
