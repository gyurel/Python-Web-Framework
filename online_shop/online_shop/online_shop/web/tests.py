from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from online_shop.web.models import Profile, Storage

UserModel = get_user_model()


class IndexViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'testuser@test.com',
        'password': '123qwert',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'gender': 'Not specified',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        return (user, profile,)

    def test_if_user_logged_in_access_granted(self):
        user, profile = self.__create_valid_user_and_profile()

        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('home page'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')

    def test_if_gets_the_storage_data_in_context(self):
        storage = Storage.objects.all()

    def test_if_redirects_to_login_if_user_not_logged_in(self):
        pass

