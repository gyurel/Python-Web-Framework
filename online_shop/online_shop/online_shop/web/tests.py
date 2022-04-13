from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse, reverse_lazy

from online_shop.web.models import Profile, Storage, Product, Cart, Favorites

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

    VALID_PRODUCT_DATA = {
        'name': 'Product',
        'product_image': 'image',
        'category': '----------------',
    }

    VALID_STORAGE_DATA = {
        'quantity': 5,
    }

    VALID_CART_DATA = {
        'quantity': 1,
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )
        product = Product.objects.create(
            **self.VALID_PRODUCT_DATA,
        )

        storage = Storage.objects.create(
            **self.VALID_STORAGE_DATA,
            product=product,
        )

        cart = Cart.objects.create(
            **self.VALID_CART_DATA,
            product=product,
            user=user,
        )

        favorites = Favorites.objects.create(
            user=user,
            product=product,
        )

        return user, profile, product, storage, cart, favorites

    def test_if_user_logged_in_access_granted(self):
        user, profile, product, storage, cart, favorites = self.__create_valid_user_and_profile()

        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('home page'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')

    def test_if_gets_the_storage_data_in_context(self):
        user, profile, product, storage, cart, favorites = self.__create_valid_user_and_profile()
        expected_storage = Storage.objects.all()
        expected_products = Product.objects.all()

        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse_lazy('home page'))

        storage = response.context['storage']
        products = response.context['products_list']

        # Check for actual profiles
        self.assertEqual(expected_storage, storage)
        self.assertEqual(expected_products, products)


    def test_if_redirects_to_login_if_user_not_logged_in(self):
        pass

