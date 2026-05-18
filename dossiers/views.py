from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Dossier, Client
from .forms import DossierForm

# ==========================================
# 1. PAGES PRINCIPALES (Vitrine & Dashboard)
# ==========================================

def landing_page(request):
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    total_dossiers = Dossier.objects.count()
    dossiers_en_cours = Dossier.objects.filter(statut='En cours').count()
    total_clients = Client.objects.count()
    
    context = {
        'total_dossiers': total_dossiers,
        'dossiers_en_cours': dossiers_en_cours,
        'total_clients': total_clients,
    }
    return render(request, 'dashboard.html', context)

# ==========================================
# 2. VUES DES DOSSIERS & CLIENTS (Affichage)
# ==========================================

class DossierListView(ListView):
    model = Dossier
    template_name = 'dossiers/dossier_list.html'
    context_object_name = 'dossiers'

class DossierDetailView(DetailView):
    model = Dossier
    template_name = 'dossiers/dossier_detail.html'
    context_object_name = 'dossier'

class ClientListView(ListView):
    model = Client
    template_name = 'dossiers/client_list.html'
    context_object_name = 'clients'

class ClientDetailView(DetailView):
    model = Client
    template_name = 'dossiers/client_detail.html'
    context_object_name = 'client'

# ==========================================
# 3. L'AJOUT DES DONNEES (Atelier 5 - Crispy)
# ==========================================

class DossierCreateView(LoginRequiredMixin, CreateView):
    model = Dossier
    form_class = DossierForm
    template_name = 'dossiers/dossier_form.html'
    success_url = reverse_lazy('dashboard')