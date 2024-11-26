from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


# Vérification de l'âge
def validate_age(value):
    age = timezone.now().year - value.year   # Verif le jour etc aussi
    if age < 15:
        raise ValidationError("Vous devez avoir au moins 15 ans pour vous inscrire.")


class User(AbstractUser):
    # Champ date de naissance avec validation d'âge
    birth_date = models.DateField(validators=[validate_age], null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
