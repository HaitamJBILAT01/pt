from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Dossier, Client, Intervention
from .forms import DossierForm, DocumentForm, ClientForm
from datetime import date
from django.db.models import Q

# ==========================================
# 1. PAGES PRINCIPALES
# ==========================================
def landing_page(request):
    return render(request, 'landing.html')

@login_required
def dashboard(request):
    total_dossiers = Dossier.objects.count()
    dossiers_en_cours = Dossier.objects.filter(statut='En cours').count()
    total_clients = Client.objects.count()
    prochaine_intervention = Intervention.objects.filter(date_intervention__gte=date.today()).order_by('date_intervention').first()
    dossiers_recents = Dossier.objects.all().order_by('-id')[:5]
    
    context = {
        'total_dossiers': total_dossiers,
        'dossiers_en_cours': dossiers_en_cours,
        'total_clients': total_clients,
        'prochaine_intervention': prochaine_intervention,
        'dossiers_recents': dossiers_recents,
    }
    return render(request, 'dashboard.html', context)

# ==========================================
# 2. VUES DES DOSSIERS & CLIENTS
# ==========================================
class DossierListView(LoginRequiredMixin, ListView):
    model = Dossier
    template_name = 'dossiers/dossier_list.html'
    context_object_name = 'dossiers'
    paginate_by = 10

    def get_queryset(self):
        queryset = Dossier.objects.all().order_by('-id')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(titre__icontains=query) | Q(id__icontains=query))
        statut = self.request.GET.get('statut')
        if statut:
            queryset = queryset.filter(statut=statut)
        return queryset

    def get_context_data(self, **kwargs):
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
    paginate_by = 5

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
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ClientDetailView(DetailView):
    model = Client
    template_name = 'dossiers/client_detail.html'
    context_object_name = 'client'

# ==========================================
# 3. L'AJOUT & MODIFICATION DES DONNEES
# ==========================================
class DossierCreateView(LoginRequiredMixin, CreateView):
    model = Dossier
    form_class = DossierForm
    template_name = 'dossiers/dossier_form.html'
    success_url = reverse_lazy('dossier_list')

class DossierUpdateView(LoginRequiredMixin, UpdateView):
    model = Dossier
    form_class = DossierForm
    template_name = 'dossiers/dossier_form.html'
    
    def get_success_url(self):
        return reverse_lazy('dossier_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context

class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'dossiers/client_form.html'
    success_url = reverse_lazy('client_list')

def importer_document(request, pk):
    dossier = get_object_or_404(Dossier, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.dossier = dossier
            document.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))