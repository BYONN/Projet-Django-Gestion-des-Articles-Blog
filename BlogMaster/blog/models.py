from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

Choix_Roles = (
    ('Lecteur','Lecteur'),
    ('Auteur','Auteur')
)

Choix_Statut = (
    ('Publié','Publié'),
    ('Brouillon','Brouillon')
)
class Utilisateur(AbstractUser):
    biographie = models.TextField()
    role = models.CharField(max_length=20, choices=Choix_Roles, default='Lecteur')
    def __str__(self):
        return self.username
    
class TypeContenu(models.Model):
    titre = models.CharField(max_length = 100)
    def __str__(self):
        return self.titre
        
class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    type_contenu = models.ForeignKey(TypeContenu, on_delete=models.CASCADE)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=Choix_Statut, default='Brouillon')
    
    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    texte = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    def __str__(self):
        return self.texte

