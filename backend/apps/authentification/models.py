from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Roles(models.TextChoices):
        DIRECTEUR = "DIRECTEUR", "Directeur"
        ENSEIGNANT = "ENSEIGNANT", "Enseignant"
        SECRETAIRE = "SECRETAIRE", "Secrétaire"
        PARENT = "PARENT", "Parent"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices
    )

    telephone = models.CharField(
        max_length=20,
        unique=True
    )

    photo = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True
    )

    actif = models.BooleanField(default=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"