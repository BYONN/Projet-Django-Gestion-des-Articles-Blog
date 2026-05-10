from django.contrib import admin
from .models import Utilisateur, TypeContenu, Article, Commentaire

# Register your models here.

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('role',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_contenu', 'user', 'statut', 'date_creation')
    list_filter = ('date_creation', 'user', 'type_contenu', 'statut')
    search_fields = ('titre', 'contenu')
    ordering = ('date_creation', 'user', 'type_contenu')


class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('texte', 'user', 'article', 'date_creation')
    list_filter = ('date_creation', 'user', 'article')
    search_fields = ('texte',)
    ordering = ('date_creation', 'user', 'article')

admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(TypeContenu)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Commentaire, CommentaireAdmin)
