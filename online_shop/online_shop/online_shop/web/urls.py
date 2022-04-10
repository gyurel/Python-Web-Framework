from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from online_shop.web.views import IndexView, ProfileDetails, EditProfile, add_to_card_view, CartView, FavoritesView, \
    add_to_favorites_view, add_one_to_articul, subtract_one_from_articul, delete_cart_articul, CheckOutView

urlpatterns = [
    path('', IndexView.as_view(), name='home page'),
    path('profile/details/<int:pk>/', ProfileDetails.as_view(), name='profile details'),
    path('profile/edit/<int:pk>/', EditProfile.as_view(), name='edit profile'),

    path('add/to/card/<int:pk>/', add_to_card_view, name='add to card'),
    path('user-cart/<int:pk>/', CartView.as_view(), name='user cart'),

    path('user-favorites/<int:pk>/', FavoritesView.as_view(), name='user favorites'),
    path('add/to/favorites/<int:pk>/', add_to_favorites_view, name='add to favorites'),

    path('add/one-to/articul/<int:pk>/', add_one_to_articul, name='add one to articul'),
    path('subtract/one-from/articul/<int:pk>/', subtract_one_from_articul, name='subtract one from articul'),
    path('delete/articul/<int:pk>/', delete_cart_articul, name=' delete cart articul'),

    path('user/checkout/<int:pk>/', CheckOutView.as_view(), name='user checkout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
