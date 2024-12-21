from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


def validate_age(value):  # regarder avec les bibli de time
    today = date.today()
    # Checks month and day
    # Second part calculates the difference between current month & day and
    # birthday month & day to determine if the reverse year has already passed
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 15:
        raise ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")


class User(AbstractUser):
    # Date of birth field with age validation
    birth_date = models.DateField(validators=[validate_age], null=False, blank=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
