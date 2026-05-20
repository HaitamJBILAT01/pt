from django import forms
from .models import Dossier

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        # Hna zedna ga3 l-champs bash Crispy y-rsemhom f HTML
        fields = ['titre', 'client', 'type_affaire', 'statut', 'partie_adverse', 'tribunal', 'description']
        
        # (Optionnel) Ila bghiti t-sgher textarea mn hna:
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }