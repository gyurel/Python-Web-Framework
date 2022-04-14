from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, Client, RequestFactory

# Create your tests here.
from django.urls import reverse, reverse_lazy

from online_shop.auth_app.models import AppUser
from online_shop.web.models import Profile, Storage, Product, Cart, Favorites
from online_shop.web.views import FavoritesView, CheckOutView, AboutView, ContactView

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

    def test_view_adds_articul_in_cart_when_it_is_not_already_added(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        NEW_PRODUCT_DATA = {
            'name': 'NewProduct',
            'product_image': 'new_image',
            'category': 'man',
        }

        new_product = Product.objects.create(**NEW_PRODUCT_DATA)
        new_storage = Storage.objects.create(quantity=10, product=new_product)

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('add to cart', kwargs={'pk': new_product.id}))

        new_articul = Cart.objects.get(pk=new_product.id)

        self.assertEqual(new_product.id, new_articul.product.id)
        self.assertEqual(302, response.status_code) # redirects home page after success

    def test_view_redirects_home_when_product_already_added_to_cart(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        new_product = Product.objects.get(pk=product.id)
        # new_storage = Storage.objects.create(quantity=10, product=new_product)

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('add to cart', kwargs={'pk': new_product.id}))

        self.assertEqual(302, response.status_code)


class AddOneToArticulInCartView(TestCase):
    def test_view_redirects_home_if_anonymous_user(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        response = self.client.get(reverse('add one to articul', kwargs={'pk': product.id}))

        self.assertEqual(302, response.status_code)

    def test_view_adds_one_to_articul_if_enough_in_storage(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        expected_quantity_in_storage = storage.quantity - 1
        expected_quantity_in_cart_articul = 2

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('add one to articul', kwargs={'pk': cart.id}))

        real_quantity_in_storage = Storage.objects.get().quantity
        real_quantity_in_cart_articul = Cart.objects.get().quantity

        self.assertEqual(302, response.status_code)
        self.assertEqual(expected_quantity_in_storage, real_quantity_in_storage)
        self.assertEqual(expected_quantity_in_cart_articul, real_quantity_in_cart_articul)


class SubtractOneFromArticulInCartView(TestCase):
    def test_view_redirects_home_if_anonymous_user(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        response = self.client.get(reverse('subtract one from articul', kwargs={'pk': product.id}))

        self.assertEqual(302, response.status_code)

    def test_view_subtracts_one_from_articul(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        expected_quantity_in_storage = storage.quantity + 1
        expected_quantity_in_cart_articul = 0

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('subtract one from articul', kwargs={'pk': cart.id}))

        real_quantity_in_storage = Storage.objects.get().quantity
        real_quantity_in_cart_articul = Cart.objects.get().quantity

        self.assertEqual(302, response.status_code)
        self.assertEqual(expected_quantity_in_storage, real_quantity_in_storage)
        self.assertEqual(expected_quantity_in_cart_articul, real_quantity_in_cart_articul)


class DeleteArticulFromCartView(TestCase):
    def test_view_redirects_home_if_anonymous_user(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()

        response = self.client.get(reverse('delete cart articul', kwargs={'pk': product.id}))

        self.assertEqual(302, response.status_code)

    def test_view_deletes_the_articul(self):
        user, profile, product, storage, cart, favorites = create_valid_user_profile_product_storage_cart_favorites()
        VALID_SECOND_PRODUCT_DATA = {
            'name': 'Product2',
            'product_image': 'image2',
            'category': 'unisex',
            'price': 11,
        }

        second_product = Product.objects.create(**VALID_SECOND_PRODUCT_DATA)
        second_storage = Storage.objects.create(quantity=5, product=second_product)
        Cart.objects.create(product=second_product, user=user)

        expected_cart = Cart.objects.first()

        self.client.login(**VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('delete cart articul', kwargs={'pk': second_product.id}))

        real_cart = Cart.objects.get()

        self.assertEqual(302, response.status_code)
        self.assertEqual(expected_cart, real_cart)


class FavoritesViewTests(TestCase):
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

    def test_if_view_redirects_to_login_when_user_not_logged_in(self):
        request = self.factory.get('user favorites')
        request.user = AnonymousUser()
        response = FavoritesView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_if_view_grants_access_when_there_is_a_logged_in_user_and_renders_correct_template(self):
        request = self.factory.get('user favorites')
        request.user = self.user
        self.client.login(**VALID_USER_CREDENTIALS)
        response = FavoritesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'favorites.html')

    def test_if_view_renders_the_right_favorites_in_context(self):
        expected_favorites = self.favorites

        request = self.factory.get('user favorites')
        request.user = self.user
        self.client.login(**VALID_USER_CREDENTIALS)
        response = FavoritesView.as_view()(request)
        self.assertEqual(response.context_data['favorites'].first(), expected_favorites)

class CheckoutViewTests(TestCase):
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

    def test_if_view_redirects_to_login_when_user_not_logged_in(self):
        request = self.factory.get('user checkout')
        request.user = AnonymousUser()
        response = FavoritesView.as_view()(request)

        self.assertEqual(response.status_code, 302)

    def test_if_view_grants_access_when_there_is_a_logged_in_user_and_renders_correct_template(self):
        request = self.factory.get('user checkout')
        request.user = self.user
        self.client.login(**VALID_USER_CREDENTIALS)
        response = CheckOutView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'checkout.html')

    def test_if_viewcontext_has_the_correct_objects_subtotal_and_total(self):
        expected_cart_object_in_context = self.cart
        expected_subtotal = self.cart.product.price * self.cart.quantity
        expected_total = expected_subtotal + 10

        request = self.factory.get('user checkout')
        request.user = self.user
        self.client.login(**VALID_USER_CREDENTIALS)
        response = CheckOutView.as_view()(request)

        existing_cart_object = response.context_data['object_list'].get()
        existing_subtotal = response.context_data['subtotal']
        existing_total = response.context_data['total']

        self.assertEqual(existing_cart_object, expected_cart_object_in_context)
        self.assertEqual(existing_subtotal, expected_subtotal)
        self.assertEqual(expected_total, existing_total)

class AboutViewTests(TestCase):
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

    def test_if_view_grants_access_when_user_anonymous(self):
        request = self.factory.get('about page')
        request.user = AnonymousUser()
        response = AboutView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'about.html')

    def test_if_view_grants_access_when_user_logged_in(self):
        request = self.factory.get('about page')
        request.user = self.user

        self.client.login(**VALID_USER_CREDENTIALS)
        response = AboutView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'about.html')

class ContactViewTests(TestCase):
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

    def test_if_view_grants_access_when_user_anonymous(self):
        request = self.factory.get('contact page')
        request.user = AnonymousUser()
        response = ContactView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'contact.html')

    def test_if_view_grants_access_when_user_logged_in(self):
        request = self.factory.get('contact page')
        request.user = self.user

        self.client.login(**VALID_USER_CREDENTIALS)
        response = ContactView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'contact.html')
