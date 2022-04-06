from django import forms

from online_shop.web.models import Profile


class EditProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Profile.GENDERS)

    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.items():
    #         fi

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user',)

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Your first name here',
                    'class': 'form-control',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Your last name here',
                    'class': 'form-control',
                }
            ),
            'date_of_birth': forms.TextInput(
                attrs={
                    'placeholder': 'Your date of birth here',
                    'class': 'form-control',
                }
            ),
            'gender': forms.TextInput(
                attrs={
                    'placeholder': 'Your gender here',
                    'class': 'form-control',
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Your address here',
                    'class': 'form-control',
                }
            ),
            'town': forms.TextInput(
                attrs={
                    'placeholder': 'Your town here',
                    'class': 'form-control',
                }
            ),
            'post_code': forms.TextInput(
                attrs={
                    'placeholder': 'Your post code here',
                    'class': 'form-control',
                }
            ),
        }
