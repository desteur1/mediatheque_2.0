from datetime import date, timedelta

from django.db import models
from django.contrib.auth.hashers import make_password,check_password

# Create your models here.


class Membre(models.Model):
    nom = models.CharField(max_length=150)
    email = models.EmailField(max_length=150,unique=True)
    mot_de_passe = models.CharField(max_length=128)
    est_bibliothecaire = models.BooleanField(default=False)

    def set_password(self,raw_password):
        self.mot_de_passe = make_password(raw_password)

    def check_password(self,raw_password):
        #self.mot_de_passe = make_password(raw_password)
        return check_password(raw_password,self.mot_de_passe)

    def __str__(self):
        return self.nom

class Media(models.Model):
    TYPE_CHOICES = [
    ('livre', 'Livre'),
    ('cd', 'CD'),
    ('dvd', 'DVD'),
    ('jeu', 'Jeu de plateau'),
    ]
    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=150)
    type_media = models.CharField(max_length=10,choices=TYPE_CHOICES)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titre


class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE,related_name="emprunts")
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name="emprunts")
    date_emprunt = models.DateField(auto_now_add=True) # set automatically
    date_retour = models.DateField(null=True,blank=True)
    rendu = models.BooleanField(default=False)


    def save(self,*args, **kwargs):
        # Si c'est un nouvel emprunt → calculer la date de retour
        if not self.pk: # nouvel emprunt
            super().save(*args, **kwargs) # remplit date_emprunt automatiquement
            if not self.date_retour:
            # Utiliser la date actuelle pour éviter le problème de None
               self.date_retour = self.date_emprunt + timedelta(days=7)
               super().save(update_fields=['date_retour'])

        else:
            super().save(*args, **kwargs)


    def est_en_retard(self):
        if self.date_retour is None:
            return False
        return (not self.rendu) and (date.today() > self.date_retour)

