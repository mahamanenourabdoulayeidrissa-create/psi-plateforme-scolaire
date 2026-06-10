from django.db import models
from django.core.validators import MinValueValidator
from apps.authentification.models import User


class Etablissement(models.Model):
    nom = models.CharField(max_length=255)
    sigle = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    adresse = models.TextField()

    logo = models.ImageField(
        upload_to="etablissements/",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Établissement"
        verbose_name_plural = "Établissements"


class AnneeScolaire(models.Model):

    libelle = models.CharField(
        max_length=20,
        unique=True
    )

    date_debut = models.DateField()
    date_fin = models.DateField()

    active = models.BooleanField(default=False)

    def __str__(self):
        return self.libelle

    class Meta:
        verbose_name = "Année scolaire"
        verbose_name_plural = "Années scolaires"


class Niveau(models.Model):

    nom = models.CharField(
        max_length=50,
        unique=True
    )

    ordre = models.PositiveIntegerField()

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ["ordre"]
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"


class Classe(models.Model):

    nom = models.CharField(max_length=50)

    niveau = models.ForeignKey(
        Niveau,
        on_delete=models.CASCADE
    )

    effectif_max = models.PositiveIntegerField(
        default=60
    )

    class Meta:
        unique_together = ("nom", "niveau")
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

    def __str__(self):
        return f"{self.nom} - {self.niveau.nom}"


class Enseignant(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    matricule = models.CharField(
        max_length=50,
        unique=True
    )

    specialite = models.CharField(max_length=100)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"


class Eleve(models.Model):

    matricule = models.CharField(
        max_length=50,
        unique=True
    )

    nom = models.CharField(max_length=100)

    prenom = models.CharField(max_length=100)

    sexe = models.CharField(
        max_length=1,
        choices=[
            ("M", "Masculin"),
            ("F", "Féminin")
        ]
    )

    date_naissance = models.DateField()

    photo = models.ImageField(
        upload_to="eleves/",
        blank=True,
        null=True
    )

    classe = models.ForeignKey(
        Classe,
        on_delete=models.PROTECT
    )

    parent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date_inscription = models.DateField()

    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    class Meta:
        verbose_name = "Élève"
        verbose_name_plural = "Élèves"


class Matiere(models.Model):

    nom = models.CharField(
        max_length=100,
        unique=True
    )

    coefficient = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    enseignant = models.ForeignKey(
        Enseignant,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"