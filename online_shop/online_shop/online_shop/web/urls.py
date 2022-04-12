from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from online_shop.web.views import IndexView, ProfileDetailsView, EditProfileView, add_to_cart_view, CartView, FavoritesView, \
    add_to_favorites_view, add_one_to_articul_in_cart_view, subtract_one_from_articul_in_cart_view, delete_cart_articul_view, CheckOutView, \
    remove_product_from_favorites_view, pay_view, AboutView, ContactView

urlpatterns = [
    path('', IndexView.as_view(), name='home page'),
    path('profile/details/<int:pk>/', ProfileDetailsView.as_view(), name='profile details'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(), name='edit profile'),

    path('add/to/card/<int:pk>/', add_to_cart_view, name='add to card'),
    path('user-cart/<int:pk>/', CartView.as_view(), name='user cart'),

    path('user-favorites/<int:pk>/', FavoritesView.as_view(), name='user favorites'),
    path('add/to/favorites/<int:pk>/', add_to_favorites_view, name='add to favorites'),
    path('remove/from/favorites/<int:pk>/', remove_product_from_favorites_view, name='remove favorit'),

    path('add/one-to/articul/<int:pk>/', add_one_to_articul_in_cart_view, name='add one to articul'),
    path('subtract/one-from/articul/<int:pk>/', subtract_one_from_articul_in_cart_view, name='subtract one from articul'),
    path('delete/articul/<int:pk>/', delete_cart_articul_view, name=' delete cart articul'),

    path('user/checkout/<int:pk>/', CheckOutView.as_view(), name='user checkout'),
    path('user/pay/<int:pk>/', pay_view, name='user pay'),

    path('about/', AboutView.as_view(), name='about page'),
    path('contact/', ContactView.as_view(), name='contact page'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
