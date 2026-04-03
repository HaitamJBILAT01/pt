from django.core.management.base import BaseCommand
from faker import Faker
import random
import datetime # ZEDNA HADI f blayst django.utils.timezone

# Kanjibo ga3 les models mn l'application dossiers w comptes
from dossiers.models import Client, Dossier, Intervention, Audience, Document
from comptes.models import CustomUser 

class Command(BaseCommand):
    help = 'Génère des fausses données pour le cabinet (Utilisateurs, Clients, Dossiers, etc.)'

    def handle(self, *args, **options):
        faker = Faker('fr_FR')
        
        # ---------------------------------------------------------
        # 1. Ncreyiw wahed Avocat w wahed Secretaire (Ila makanoch)
        # ---------------------------------------------------------
        avocat, created = CustomUser.objects.get_or_create(
            username='maitre_fake',
            defaults={
                'first_name': faker.first_name(),
                'last_name': faker.last_name(),
                'email': faker.email(),
                'role': 'Avocat',
                'is_staff': True
            }
        )
        if created:
            avocat.set_password('admin123')
            avocat.save()
            self.stdout.write(self.style.SUCCESS(f"Avocat créé: {avocat.username}"))

        # ---------------------------------------------------------
        # 2. Ncreyiw 5 dyal les Clients (CustomUser + Client Profile)
        # ---------------------------------------------------------
        clients_crees = []
        for i in range(5):
            # A. Kan-creyiw l'User
            user_client = CustomUser.objects.create_user(
                username=f"client_{faker.user_name()}_{i}",
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                password='password123',
                role='Client'
            )
            
            # B. Kan-creyiw l'Profil Client w kanrbtouh b l'User
            client_profile = Client.objects.create(
                user=user_client,
                telephone=faker.phone_number(),
                adresse=faker.address()
            )
            clients_crees.append(client_profile)
            self.stdout.write(f"Client créé: {user_client.first_name} {user_client.last_name}")

        # ---------------------------------------------------------
        # 3. Ncreyiw 10 Dossier w nzidou fihom Audiences/Documents
        # ---------------------------------------------------------
        statuts = ['En cours', 'Clôturé', 'Suspendu']
        
        for i in range(10):
            dossier = Dossier.objects.create(
                titre=faker.sentence(nb_words=5).replace('.', ''),
                description=faker.text(max_nb_chars=300),
                statut=random.choice(statuts),
                client=random.choice(clients_crees), # Kan3zlo client mn dok l 5
                avocat=avocat # Kan-affectiw l'avocat li sawbna lfoq
            )
            
            # Nzidou Intervention wla joj l had l'dossier (BDDLNA tzinfo HNA)
            for _ in range(random.randint(1, 2)):
                Intervention.objects.create(
                    dossier=dossier,
                    titre=faker.catch_phrase(),
                    description=faker.text(max_nb_chars=150),
                    date_intervention=faker.date_time_between(start_date='-1y', end_date='now', tzinfo=datetime.timezone.utc) 
                )

            # Nzidou Audience l had l'dossier (BDDLNA tzinfo HNA)
            Audience.objects.create(
                dossier=dossier,
                date_audience=faker.date_time_between(start_date='now', end_date='+6m', tzinfo=datetime.timezone.utc),
                tribunal=faker.company() + " Tribunal",
                salle=f"Salle {faker.random_int(min=1, max=10)}",
                notes=faker.text(max_nb_chars=100)
            )

            # Nzidou Document kdoub
            Document.objects.create(
                dossier=dossier,
                titre=f"Document_{faker.word()}.pdf"
            )
            
            self.stdout.write(f"Dossier {i+1} crée avec success ")

        self.stdout.write(self.style.SUCCESS('\n DONE'))