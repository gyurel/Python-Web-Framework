from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import datetime


def min_length_validator(value):
    min_length = 2
    if len(value) < min_length:
        raise ValidationError('Name shorter than expected!')


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            # Invalid case
            raise ValidationError('Value must contain only letters')


@deconstructible
class MaxFileSizeInMbValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        filesize = value.file.size
        if filesize > self.max_size * 1024 * 1024:
            raise ValidationError("Max file size is %sMB" % str(self.max_size))


def value_less_than_zero(value):
    if value < 0:
        raise ValidationError('Value must be greater than zero!')


def age_greater_than_120(value):
    if value > 120:
        raise ValidationError('Value must be less than 120')


@deconstructible
class MinDateValidator:
    def __init__(self, years_from_now):
        self.years_form_now = years_from_now

    def __call__(self, value):
        max_time_allowed_from_now_in_days = self.years_form_now * 365.24

        td = datetime.date.today() - value

        if max_time_allowed_from_now_in_days < td.days:
            raise ValidationError("Age should be not greater than 120")


@deconstructible
class MaxDateValidator:
    def __init__(self, current_time):
        self.current_time = current_time

    def __call__(self, value):
        if value > self.current_time:
            raise ValidationError("Date should be earlier than the current!")