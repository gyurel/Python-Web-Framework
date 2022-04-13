from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse, reverse_lazy

from online_shop.web.models import Profile, Storage, Product, Cart, Favorites

UserModel = get_user_model()

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


def create_user(**credentials):
    return UserModel.objects.create_user(**credentials)


def create_valid_user_and_profile():
    user = create_user(**VALID_USER_CREDENTIALS)
    profile = Profile.objects.create(
        **VALID_PROFILE_DATA,
        user=user,
    )
    product = Product.objects.create(
        **VALID_PRODUCT_DATA,
    )

    storage = Storage.objects.create(
        **VALID_STORAGE_DATA,
        product=product,
    )

    cart = Cart.objects.create(
        **VALID_CART_DATA,
        product=product,
        user=user,
    )

    favorites = Favorites.objects.create(
        user=user,
        product=product,
    )

    return user, profile, product, storage, cart, favorites


class IndexViewTests(TestCase):

    def test_if_user_logged_in_access_granted(self):
        user, profile, product, storage, cart, favorites = create_valid_user_and_profile()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('home page'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')

    def test_if_gets_the_storage_data_in_context(self):
        user, profile, product, storage, cart, favorites = create_valid_user_and_profile()
        expected_storage = Storage.objects.all().get()
        expected_products = Product.objects.all().get()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse_lazy('home page'))

        context_storage = response.context['storage'].get()
        context_products = response.context['products_list'].get()

        self.assertEqual(expected_storage, context_storage)
        self.assertEqual(expected_products, context_products)

    def test_if_redirects_to_login_if_user_not_logged_in(self):

        user, profile, product, storage, cart, favorites = create_valid_user_and_profile()

        response = self.client.get(reverse('home page'))

        self.assertEqual(302, response.status_code)


class ProfileDetailsView(TestCase):

    def test_if_user_logged_in_access_granted(self):
        user, profile, product, storage, cart, favorites = create_valid_user_and_profile()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={'pk': user.id}))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'profile-details.html')

    def test_if_the_view_redirects_to_login_if_user_not_logged_in(self):
        user, profile, product, storage, cart, favorites = create_valid_user_and_profile()

        # self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={'pk': user.id}))

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, '/', 302, 302)

    def test_assert_when_logged_in_user_the_right_profile_in_context(self):
        user, profile, product, storage, cart, favorites = create_valid_user_and_profile()

        expected_profile = Profile.objects.all().get()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse_lazy('profile details', kwargs={'pk': user.id}))

        context_profile = response.context['profile']

        self.assertEqual(expected_profile, context_profile)

