from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse, reverse_lazy

from online_shop.auth_app.models import AppUser
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


def create_valid_user_profile_product_storage_cart_favorites():
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
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('home page'))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'index.html')

    def test_if_gets_the_storage_data_in_context(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()
        expected_storage = Storage.objects.all().get()
        expected_products = Product.objects.all().get()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse_lazy('home page'))

        context_storage = response.context['storage'].get()
        context_products = response.context['products_list'].get()

        self.assertEqual(expected_storage, context_storage)
        self.assertEqual(expected_products, context_products)

    def test_if_redirects_to_login_if_user_not_logged_in(self):

        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        response = self.client.get(reverse('home page'))

        self.assertEqual(302, response.status_code)


class ProfileDetailsViewTests(TestCase):

    def test_if_user_logged_in_access_granted(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('profile details', kwargs={'pk': user.id}))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'profile-details.html')

    def test_if_the_view_redirects_to_login_if_user_not_logged_in(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        response = self.client.get(reverse('profile details', kwargs={'pk': user.id}))

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, '/', 302, 302)

    def test_assert_when_logged_in_user_the_right_profile_in_context(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        expected_profile = Profile.objects.all().get()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse_lazy('profile details', kwargs={'pk': user.id}))

        context_profile = response.context['profile']

        self.assertEqual(expected_profile, context_profile)


class EditProfileViewTests(TestCase):

    def test_if_user_logged_in_access_granted(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('edit profile', kwargs={'pk': user.id}))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'profile-edit.html')

    def test_if_the_view_redirects_to_login_if_user_not_logged_in(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        response = self.client.get(reverse('edit profile', kwargs={'pk': user.id}))

        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, '/', 302, 302)

    def test_assert_when_logged_in_user_the_right_profile_in_context(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        expected_profile = Profile.objects.all().get()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse_lazy('edit profile', kwargs={'pk': user.id}))

        context_profile = response.context['profile']

        self.assertEqual(expected_profile, context_profile)

    def test_edit_profile_when_all_data_valid(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        NEW_VALID_PROFILE_DATA = {
            'first_name': 'Newtestuser',
            'gender': 'Man',
        }

        self.client.login(**VALID_USER_CREDENTIALS)

        response_get = self.client.get(reverse_lazy('edit profile', kwargs={'pk': user.id}))

        response_post = self.client.post(
            reverse('edit profile', kwargs={'pk': user.id}),
            {**VALID_USER_CREDENTIALS, **NEW_VALID_PROFILE_DATA},
        )

        profile = Profile.objects.first()

        self.assertEqual(200, response_get.status_code)
        self.assertIsNotNone(profile)
        self.assertEqual(200, response_post.status_code)
        # self.assertEqual(NEW_VALID_PROFILE_DATA['first_name'], profile.first_name)
        # self.assertEqual(NEW_VALID_PROFILE_DATA['gender'], profile.gender)


class CartViewTests(TestCase):
    def test_if_user_logged_in_access_granted(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('user cart', kwargs={'pk': user.id}))

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'cart.html')

    def test_if_the_view_redirects_to_login_if_user_not_logged_in(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        response = self.client.get(reverse('user cart', kwargs={'pk': user.id}))

        self.assertEqual(302, response.status_code)
        # self.assertRedirects(response, 'login user', 302, 200)

    def test_assert_when_logged_in_user_the_right_user_and_cart_in_context(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        expected_cart = Cart.objects.all().first()
        expected_user = AppUser.objects.first()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse_lazy('user cart', kwargs={'pk': user.id}))

        context_cart = response.context['cart'].first()
        context_user = response.context['user']

        self.assertEqual(expected_cart, context_cart)
        self.assertEqual(expected_user, context_user)


class AddToCartViewTests(TestCase):

    def test_view_redirects_home_if_anonymous_user(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        response = self.client.get(reverse('add to cart', kwargs={'pk': product.id}))

        self.assertEqual(302, response.status_code)

    def test_view_redirects_when_articul_already_in_cart(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('add to cart', kwargs={'pk': product.id}))

        self.assertEqual(302, response.status_code)

