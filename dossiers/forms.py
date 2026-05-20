from django import forms
from .models import Dossier, Document, Client

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        # Hna zedna ga3 l-champs bash Crispy y-rsemhom f HTML
        fields = ['titre', 'client', 'type_affaire', 'statut', 'partie_adverse', 'tribunal', 'description']
        
        # (Optionnel) Ila bghiti t-sgher textarea mn hna:
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['titre', 'fichier']        

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['prenom', 'nom', 'telephone', 'adresse', 'photo_cin']        