from django import forms
from .models import Dossier

class DossierForm(forms.ModelForm):
    class Meta:
        model = Dossier
        # Hna kan-goulou l'Django achno homa l'khaanat li bghinahom ybano f l'Formulaire
        fields = ['titre', 'client', 'description', 'statut'] 
        
        # Zwaq sghir bash l'Formulaire yban zwin
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }