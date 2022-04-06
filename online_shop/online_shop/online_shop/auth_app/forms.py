from django.contrib.auth import forms as auth_forms, get_user_model
from django import forms

# from common.helpers import BootstrapFormMixin
from online_shop.auth_app.models import AppUser
from online_shop.web.models import Profile

UserModel = get_user_model()


# class UserRegistrationForm(auth_forms.UserCreationForm):
#     class Meta:
#         model = UserModel
#         fields = ('username',)


class UserRegistrationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=25)

    def clean_first_name(self):
        return self.cleaned_data['first_name']

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            self.clean_first_name(),
            user=user,
        )
        if commit:
            profile.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name')

        widgets = {
            'email': forms.TextInput(
                attrs={
                    'placeholder': 'Your email here',
                    'class': 'form-control',
                }
            ),
            'password1': forms.TextInput(
                attrs={
                    'placeholder': 'Your password here',
                    'class': 'form-control',
                }
            ),
            'password2': forms.TextInput(
                attrs={
                    'placeholder': 'Repeat your password',
                    'class': 'form-control',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Your first name here',
                    'class': 'form-control',
                }
            )
        }


class EditUserForm(auth_forms.PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2',)

        widgets = {
            'old_password': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your current password here',
                }
            ),
            'new_password1': forms.PasswordInput(
                attrs={
                    'placeholder': 'Your new password here',
                    'class': 'form-control',
                }
            ),
            'new_password2': forms.PasswordInput(
                attrs={
                    'placeholder': 'Repeat your new password',
                    'class': 'form-control',
                }
            ),
        }


class DeleteUserForm(forms.ModelForm):
    # email = forms.CharField(max_length=25)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['disabled'] = 'disabled'
            field.required = False

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = get_user_model()
        fields = ('email',)

        # widgets = {
        #     'email': forms.TextInput(
        #         attrs={
        #             'class': 'form-control',
        #             'label': 'User'
        #         }
        #     ),
        # }

        labels = {
            'email': 'User:',
        }

# class DeleteUserForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for _, field in self.fields.items():
#             field.widget.attrs['disabled'] = 'disabled'
#             field.required = False
#
#     def save(self, commit=True):
#         self.instance.delete()
#         return self.instance
#
#     class Meta:
#         model = AppUser
#         fields = ('email',)
