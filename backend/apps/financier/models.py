from django.db import models
from apps.administration.models import Eleve


class TrancheScolarite(models.Model):

    libelle = models.CharField(max_length=100)

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    date_limite = models.DateField()

    def __str__(self):
        return self.libelle


class Paiement(models.Model):

    MODES = (
        ("MOMO", "Mobile Money"),
        ("WAVE", "Wave"),
        ("ESPECES", "Espèces")
    )

    eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE
    )

    tranche = models.ForeignKey(
        TrancheScolarite,
        on_delete=models.PROTECT
    )

    montant = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    mode = models.CharField(
        max_length=20,
        choices=MODES
    )

    reference = models.CharField(
        max_length=100,
        unique=True
    )

    date_paiement = models.DateTimeField(
        auto_now_add=True
    )

    statut = models.CharField(
        max_length=20,
        default="VALIDE"
    )

    def __str__(self):
        return self.reference


class Recu(models.Model):

    paiement = models.OneToOneField(
        Paiement,
        on_delete=models.CASCADE
    )

    numero = models.CharField(
        max_length=100,
        unique=True
    )

    pdf = models.FileField(
        upload_to="recus/"
    )

    def __str__(self):
        return self.numero


class RelanceImpaye(models.Model):

    eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    date_envoi = models.DateTimeField(
        auto_now_add=True
    )

    sms_envoye = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"Relance {self.eleve}"