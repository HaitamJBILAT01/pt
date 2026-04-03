from django.db import models
from django.conf import settings

class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile_client')
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    photo_cin = models.ImageField(upload_to='clients/cin/', null=True, blank=True, verbose_name="Photo CIN")
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Client: {self.user.username}"

class Dossier(models.Model):
    STATUT_CHOICES = (
        ('En cours', 'En cours'),
        ('Clôturé', 'Clôturé'),
        ('Suspendu', 'Suspendu'),
    )
    titre = models.CharField(max_length=250, verbose_name="Titre du dossier")
    description = models.TextField()
    statut = models.CharField(max_length=50, choices=STATUT_CHOICES, default='En cours')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='dossiers')
    avocat = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='dossiers_en_charge')

    def __str__(self):
        return self.titre

class Intervention(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='interventions')
    titre = models.CharField(max_length=250)
    description = models.TextField()
    document_joint = models.FileField(upload_to='interventions/documents/', null=True, blank=True)
    date_intervention = models.DateTimeField()

    def __str__(self):
        return f"{self.titre} - {self.dossier.titre}"

class Audience(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='audiences')
    date_audience = models.DateTimeField()
    tribunal = models.CharField(max_length=150)
    salle = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Audience: {self.tribunal} - {self.dossier.titre}"

class Document(models.Model):
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='documents')
    titre = models.CharField(max_length=250)
    fichier = models.FileField(upload_to='dossiers/documents/') 
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre