from django.urls import path

from online_shop.auth_app.views import UserRegistrationView, UserLoginView, UserLogoutView, EditUserView, \
    SuccessfullyEditedUser, delete_user_view

urlpatterns = (
    path('register/', UserRegistrationView.as_view(), name='register user'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('user/edit/<int:pk>/', EditUserView.as_view(), name='edit user'),
    path('user/edit/success/', SuccessfullyEditedUser.as_view(), name='edit user success'),
    path('user/delete/<int:pk>/', delete_user_view, name='delete user')
)
