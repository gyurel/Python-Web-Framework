from django.test import TestCase

# Create your tests here.


class ProfileDetailsViewTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'testuser',
        'password': '123qwert',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'picture': 'http://test.picture/url.png',
        'date_of_birth': date(1990, 4, 13),
    }

    VALID_PET_DATA = {
        'name': 'The pet',
        'type': Pet.CAT,
    }

    VALID_PET_PHOTO_DATA = {
        'photo': 'asd.jpg',
        'publication_date': date.today(),
    }