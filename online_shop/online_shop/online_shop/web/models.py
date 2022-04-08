from django.db import models
import datetime

from common.validators import min_length_validator, validate_only_letters, MaxFileSizeInMbValidator, \
    age_greater_than_120, MinDateValidator, MaxDateValidator
from django.core import validators
from online_shop.auth_app.models import AppUser
from online_shop.settings import STATICFILES_DIRS, MEDIA_ROOT, BASE_DIR, STATIC_URL


# Create your models here.


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 25
    LAST_NAME_MAX_LENGTH = 25

    DATE_OF_BIRTH_MIN_VALUE_YEARS = datetime.date.today()
    DATE_OF_BIRTH_MAX_VALUE_YEARS = 120

    ADDRESS_MIN_LENGTH = 5
    ADDRESS_MAX_LENGTH = 50

    TOWN_MIN_LENGTH = 3
    TOWN_MAX_LENGTH = 25

    POST_CODE_MAX_DIGITS = 4
    POST_CODE_MIN_VALUE = 1000
    POST_CODE_MAX_VALUE = 9999
    POST_CODE_TOO_SHORT_MESSAGE = 'Post code should be greater than 999'
    POST_CODE_TOO_BIG_VALUE_MESSAGE = 'Value should not exceed 9999'

    GENDER_NOT_SPECIFIED = "Not specified"
    GENDER_MAN = "Man"
    GENDER_WOMAN = "Woman"
    GENDER_DONT_WONT_TO_SECIFY = "Don't want to specify"
    GENDER_MAX_LENGTH = max([len(x) for x in [GENDER_NOT_SPECIFIED, GENDER_MAN, GENDER_WOMAN, GENDER_DONT_WONT_TO_SECIFY]])
    GENDERS = [(x, x) for x in [GENDER_NOT_SPECIFIED, GENDER_MAN, GENDER_WOMAN, GENDER_DONT_WONT_TO_SECIFY]]

    # IMAGE_UPLOAD_DIR = '/mediafiles/profiles/'
    PROFILE_IMAGE_UPLOAD_DIR = f'{MEDIA_ROOT}\\profiles\\'

    MAX_FILE_SIZE = 5

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            min_length_validator,
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        null=True,
        blank=True,
        validators=(
            min_length_validator,
            validate_only_letters,
        )
    )

    date_of_birth = models.DateField(
        null=True,
        validators=(
            # age_less_than_zero,
            MaxDateValidator(DATE_OF_BIRTH_MIN_VALUE_YEARS),
            MinDateValidator(DATE_OF_BIRTH_MAX_VALUE_YEARS),
        )
    )

    gender = models.CharField(
        max_length=GENDER_MAX_LENGTH,
        null=False,
        default=GENDER_NOT_SPECIFIED,
        # default=GENDER_NOT_SPEDIFIED,
        choices=GENDERS,
    )

    address = models.CharField(
        max_length=ADDRESS_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(ADDRESS_MIN_LENGTH),
        ),
        null=True,
        blank=True,
    )

    town = models.CharField(
        max_length=TOWN_MAX_LENGTH,
        validators=(
            validators.MinLengthValidator(TOWN_MIN_LENGTH),
        ),
        null=True,
        blank=True,
    )

    post_code = models.DecimalField(
        max_digits=POST_CODE_MAX_DIGITS,
        decimal_places=0,
        validators=(
            validators.MinValueValidator(POST_CODE_MIN_VALUE, message=POST_CODE_TOO_SHORT_MESSAGE),
            validators.MaxValueValidator(POST_CODE_MAX_VALUE, message=POST_CODE_TOO_BIG_VALUE_MESSAGE),
        ),
        null=True,
        blank=True,
    )

    profile_image = models.ImageField(
        # default=f'{BASE_DIR / STATIC_URL}\\images\\user.png',
        null=True,
        upload_to=PROFILE_IMAGE_UPLOAD_DIR,
        validators=(
            MaxFileSizeInMbValidator(MAX_FILE_SIZE),
        )
    )

    user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    @property
    def full_name(self):
        if self.last_name:
            return f'{self.first_name} {self.last_name}'
        return self.first_name

    @property
    def age(self):
        if self.date_of_birth:
            return datetime.datetime.now().year - self.date_of_birth.year


class Product(models.Model):
    PRODUCT_NAME_MAX_LENGTH = 25

    CHOSE_CATEGORY = '----------------'
    CATEGORY_MAN = 'Man'
    CATEGORY_WOMAN = 'Woman'
    CATEGORY_UNISEX = 'Unisex'
    CATEGORY_MAX_LENGTH = max([len(x) for x in [CHOSE_CATEGORY, CATEGORY_MAN, CATEGORY_WOMAN, CATEGORY_UNISEX]])
    CATEGORIES = [(x, x) for x in [CHOSE_CATEGORY, CATEGORY_MAN, CATEGORY_WOMAN, CATEGORY_UNISEX]]

    MIN_PRICE_MESSAGE = 'Price may not be less than zero!'
    PRICE_MIN_VALUE = 0
    PRICE_MAX_DIGITS = 4
    PRICE_DECIMAL_PLACES = 2

    PRODUCT_IMAGE_UPLOAD_DIR = f'{MEDIA_ROOT}\\products\\'
    MAX_FILE_SIZE = 5

    name = models.CharField(
        max_length=PRODUCT_NAME_MAX_LENGTH,
        unique=True,
        null=False,
    )

    product_image = models.ImageField(
        null=True,
        upload_to=PRODUCT_IMAGE_UPLOAD_DIR,
        validators=(
            MaxFileSizeInMbValidator(MAX_FILE_SIZE),
        )
    )

    category = models.CharField(
        max_length=CATEGORY_MAX_LENGTH,
        choices=CATEGORIES,
        default=CHOSE_CATEGORY,
        null=False,
    )

    price = models.DecimalField(
        max_digits=PRICE_MAX_DIGITS,
        decimal_places=PRICE_DECIMAL_PLACES,
        validators=(
            validators.MinValueValidator(PRICE_MIN_VALUE, message=MIN_PRICE_MESSAGE),
        ),
        null=True,
        blank=True,
    )


class Storage(models.Model):
    DEFAULT_PRODUCT_QUANTITY = 0
    MIN_PRODUCT_QUANTITY = 0
    MIN_PRODUCT_MESSAGE = 'The quantity can not be less than zero!'

    quantity = models.IntegerField(
        default=DEFAULT_PRODUCT_QUANTITY,
        null=False,
        validators=(
            validators.MinValueValidator(MIN_PRODUCT_QUANTITY, message=MIN_PRODUCT_MESSAGE),
        )
    )

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class Cart(models.Model):
    DEFAULT_QUANTITY = 1
    MIN_QUANTITY = 0
    MIN_MESSAGE = 'The quantity can not be less than zero!'
    CHOICES = [(x, x) for x in range(0, 11)]

    quantity = models.IntegerField(
        default=DEFAULT_QUANTITY,
        null=False,
        choices=CHOICES,
        validators=(
            validators.MinValueValidator(MIN_QUANTITY, message=MIN_MESSAGE),
        )
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )


class Favorites(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
