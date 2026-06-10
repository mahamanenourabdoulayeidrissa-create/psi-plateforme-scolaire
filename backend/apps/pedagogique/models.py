from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.administration.models import (
    Eleve,
    Matiere,
    AnneeScolaire
)


class Evaluation(models.Model):

    TYPES = (
        ("DEVOIR", "Devoir"),
        ("COMPOSITION", "Composition"),
        ("EXAMEN", "Examen"),
    )

    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE
    )

    type_evaluation = models.CharField(
        max_length=20,
        choices=TYPES
    )

    trimestre = models.PositiveIntegerField()

    date_evaluation = models.DateField()

    coefficient = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.matiere.nom} - {self.type_evaluation}"


class Note(models.Model):

    eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE
    )

    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE
    )

    note = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(20)
        ]
    )

    class Meta:
        unique_together = (
            "eleve",
            "evaluation"
        )

    def __str__(self):
        return f"{self.eleve} - {self.note}"


class Absence(models.Model):

    eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE
    )

    date_absence = models.DateField()

    justifiee = models.BooleanField(default=False)

    motif = models.TextField(blank=True)

    def __str__(self):
        return f"{self.eleve} - {self.date_absence}"


class Bulletin(models.Model):

    eleve = models.ForeignKey(
        Eleve,
        on_delete=models.CASCADE
    )

    annee = models.ForeignKey(
        AnneeScolaire,
        on_delete=models.CASCADE
    )

    trimestre = models.PositiveIntegerField()

    moyenne = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    rang = models.PositiveIntegerField()

    pdf = models.FileField(
        upload_to="bulletins/"
    )

    date_generation = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Bulletin {self.eleve}"