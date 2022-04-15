from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client, RequestFactory

# Create your tests here.
from django.urls import reverse

from online_shop.auth_app.views import UserRegistrationView, UserLoginView, EditUserView
from online_shop.web.models import Profile, Storage, Product, Cart, Favorites
from online_shop.web.tests import create_user, create_valid_user_profile_product_storage_cart_favorites

# Create your tests here.
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
    'price': 5,
}

VALID_STORAGE_DATA = {
    'quantity': 5,
}

VALID_CART_DATA = {
    'quantity': 1,
}

class UserRegistrationViewTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            **VALID_PROFILE_DATA,
            user=self.user,
        )
        self.product = Product.objects.create(
            **VALID_PRODUCT_DATA,
        )

        self.storage = Storage.objects.create(
            **VALID_STORAGE_DATA,
            product=self.product,
        )

        self.cart = Cart.objects.create(
            **VALID_CART_DATA,
            product=self.product,
            user=self.user,
        )

        self.favorites = Favorites.objects.create(
            user=self.user,
            product=self.product,
        )

        self.client = Client()

    def test_if_view_redirects_to_home_when_user_authenticated(self):
        request = self.factory.get('register user')
        request.user = self.user
        response = UserRegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_if_view_redirects_to_home_when_user_authenticated_and_logged_in(self):
        request = self.factory.get('register user')
        request.user = self.user
        self.client.login(**VALID_USER_CREDENTIALS)
        response = UserRegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home page'))

    def test_if_view_grants_access_when_there_is_an_anonymous_user_and_renders_correct_template(self):
        request = self.factory.get('register user')
        request.user = AnonymousUser()

        response = UserRegistrationView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'auth/register.html')


class UserLoginViewTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            **VALID_PROFILE_DATA,
            user=self.user,
        )
        self.product = Product.objects.create(
            **VALID_PRODUCT_DATA,
        )

        self.storage = Storage.objects.create(
            **VALID_STORAGE_DATA,
            product=self.product,
        )

        self.cart = Cart.objects.create(
            **VALID_CART_DATA,
            product=self.product,
            user=self.user,
        )

        self.favorites = Favorites.objects.create(
            user=self.user,
            product=self.product,
        )

        self.client = Client()

    def test_if_view_redirects_to_home_when_user_authenticated(self):
        request = self.factory.get('login user')
        request.user = self.user
        response = UserLoginView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_if_view_redirects_to_home_when_user_authenticated_and_logged_in(self):
        request = self.factory.get('login user')
        request.user = self.user
        self.client.login(**VALID_USER_CREDENTIALS)
        response = UserLoginView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_if_view_grants_access_when_there_is_an_anonymous_user_and_renders_correct_template(self):
        request = self.factory.get('login user')
        request.user = AnonymousUser()

        response = UserLoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'auth/login.html')


class EditUserViewTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = create_user(**VALID_USER_CREDENTIALS)
        self.profile = Profile.objects.create(
            **VALID_PROFILE_DATA,
            user=self.user,
        )
        self.product = Product.objects.create(
            **VALID_PRODUCT_DATA,
        )

        self.storage = Storage.objects.create(
            **VALID_STORAGE_DATA,
            product=self.product,
        )

        self.cart = Cart.objects.create(
            **VALID_CART_DATA,
            product=self.product,
            user=self.user,
        )

        self.favorites = Favorites.objects.create(
            user=self.user,
            product=self.product,
        )

        self.client = Client()

    def test_if_view_redirects_to_home_when_user_not_authenticated(self):
        request = self.factory.get('edit user')

        request.user = AnonymousUser()
        response = EditUserView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_if_view_redirects_to_home_when_user_authenticated_and_logged_in(self):
        request = self.factory.get('edit user')
        request.user = self.user

        self.client.login(**VALID_USER_CREDENTIALS)

        response = EditUserView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'auth/edit-user.html')


class DeleteUserViewTests(TestCase):

    def test_if_user_logged_in_access_granted(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('delete user', kwargs={'pk': user.id}))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'auth/delete-user.html')
