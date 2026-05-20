from django.contrib import admin
from django.urls import path
from dossiers.views import landing_page, dashboard, DossierListView, DossierDetailView, ClientListView, ClientDetailView, DossierCreateView, importer_document
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # L'Accueil Public (Vitrine)
    path('', landing_page, name='landing'),
    
    # L'Espace Privé (Dashboard)
    path('dashboard/', dashboard, name='dashboard'),
    
    # dossier
    path('dossiers/', DossierListView.as_view(), name='dossier_list'),
    path('dossier/<int:pk>/', DossierDetailView.as_view(), name='dossier_detail'),
    path('dossier/ajouter/', DossierCreateView.as_view(), name='dossier_create'),
    
    # client
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    
    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name='comptes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('dossier/<int:pk>/importer/', importer_document, name='importer_document'),

    
]