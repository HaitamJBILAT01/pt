from django.contrib import admin
from .models import Client, Dossier, Intervention , Audience, Document

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'telephone', 'date_ajout')

@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = ('titre', 'client', 'avocat', 'statut', 'date_creation')
    list_filter = ('statut', 'avocat')

@admin.register(Intervention)
class InterventionAdmin(admin.ModelAdmin):
    list_display = ('titre', 'dossier', 'date_intervention')



@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    list_display = ('dossier', 'date_audience', 'tribunal', 'salle')
    list_filter = ('tribunal', 'date_audience')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('titre', 'dossier', 'date_creation')