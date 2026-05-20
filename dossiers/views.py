from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404, redirect

from .models import Dossier, Client, Intervention
from .forms import DossierForm, DocumentForm, ClientForm

from datetime import date

from django.db.models import Q


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
    
    # 🆕 Khedma jdida: Jib awel intervention jayya mn l-yoma l-lfouq
    prochaine_intervention = Intervention.objects.filter(date_intervention__gte=date.today()).order_by('date_intervention').first()
    
    # Akhir 5 dossiers
    dossiers_recents = Dossier.objects.all().order_by('-id')[:5]
    
    context = {
        'total_dossiers': total_dossiers,
        'dossiers_en_cours': dossiers_en_cours,
        'total_clients': total_clients,
        'prochaine_intervention': prochaine_intervention, # Zdnaha hna
        'dossiers_recents': dossiers_recents,
    }
    return render(request, 'dashboard.html', context)

# ==========================================
# 2. VUES DES DOSSIERS & CLIENTS (Affichage)
# ==========================================

class DossierListView(LoginRequiredMixin, ListView):
    model = Dossier
    template_name = 'dossiers/dossier_list.html'
    context_object_name = 'dossiers'
    paginate_by = 10

    def get_queryset(self):
        # 1. N-jibou ga3 l-dossiers m-stfin mn j-jdid l-qdim
        queryset = Dossier.objects.all().order_by('-id')
        
        # 2. L-Qbiyd dyal Recherche (Search) b Titre wla ID
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(titre__icontains=query) | 
                Q(id__icontains=query)
            )
            
        # 3. L-Qbiyd dyal l-Filtre (Statut)
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
            
        return queryset

    def get_context_data(self, **kwargs):
        # 4. N-ssifto 'q' w 'statut' l'HTML bash y-bqaw m-ktoubin f l'Input mnin n-actualisiw
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_statut'] = self.request.GET.get('statut', '')
        return context
    

class DossierDetailView(DetailView):
    model = Dossier
    template_name = 'dossiers/dossier_detail.html'
    context_object_name = 'dossier'
    

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'dossiers/client_list.html'
    context_object_name = 'clients'
    paginate_by = 5  # Hna drna Pagination b 5 

    def get_queryset(self):
        queryset = Client.objects.all().order_by('-id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nom__icontains=query) | 
                Q(prenom__icontains=query) |
                Q(telephone__icontains=query)
            )
        return queryset
        
    def get_context_data(self, **kwargs):
        # Bash tbqa l-ktaba m-7foda f l-Input d'Recherche
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

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




def importer_document(request, pk):
    # Kanjbdou l'dossier li bghina nzidou fih l'fichier
    dossier = get_object_or_404(Dossier, pk=pk)
    
    if request.method == 'POST':
        # Meli katkon image wla fichier, Dima khasna (request.POST, request.FILES)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # Kanssjou l'document wlakin makan-validiwch f l'base de données (commit=False)
            document = form.save(commit=False)
            # Kanrbtoh m3a l'dossier dyalna
            document.dossier = dossier
            # 3ad kanssjlo kolchi
            document.save()
            
    # Kan-redirigiw l'utilisateur l'nfs la page mn b3d l'ajout
    return redirect(request.META.get('HTTP_REFERER', '/'))


class DossierUpdateView(LoginRequiredMixin, UpdateView):
    model = Dossier
    form_class = DossierForm
    template_name = 'dossiers/dossier_form.html' # Kan-khedmou b nfs d-Design l-Wa3er!
    
    def get_success_url(self):
        # Mnin l'Avocat y-modifier d-dossier, Django ghay-rjj3o l'Page d-Détails bash y-shouf t-taghyirat
        return reverse_lazy('dossier_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        # Hadi ghir bash n-goulou l'HTML rahna f wde3 "Modification" machi "Ajout"
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context
    

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'dossiers/client_form.html'
    success_url = reverse_lazy('client_list')    