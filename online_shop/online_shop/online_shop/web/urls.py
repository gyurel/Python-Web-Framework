from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from online_shop.web.views import IndexView, ProfileDetails, EditProfile, add_to_card_view, CartView

urlpatterns = [
    path('', IndexView.as_view(), name='home page'),
    path('profile/details/<int:pk>/', ProfileDetails.as_view(), name='profile details'),
    path('profile/edit/<int:pk>/', EditProfile.as_view(), name='edit profile'),
    path('add/to/card/<int:pk>/', add_to_card_view, name='add to card'),
    path('user-cart/<int:pk>/', CartView.as_view(), name='user cart')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
