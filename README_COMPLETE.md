# 🚀 EasyInvoice - Plateforme complète de génération de documents

## 📋 Vue d'ensemble

**EasyInvoice** est une application Django modulaire qui permet de générer facilement :
- 📄 **Factures PDF professionnelles** (module CORE)
- 📦 **Étiquettes d'expédition** (module TICKET)

Le système est conçu pour les **freelances, entrepreneurs individuels et petites entreprises** qui ont besoin de créer rapidement des documents conformes aux normes françaises.

---

## ✨ Fonctionnalités principales

### Module EasyInvoice (Factures)
✅ Génération de factures PDF professionnelles  
✅ Conformité légale française (TVA, SIRET, RCS, mentions obligatoires)  
✅ Support de la franchise de TVA (article 293 B du CGI)  
✅ Gestion des pénalités de retard et frais de recouvrement  
✅ Mention autoliquidation (BTP)  
✅ Multi-articles avec ajout/suppression dynamique (HTMX)  
✅ Design responsive et moderne  
✅ Pas de base de données requise pour l'utilisation simple  

### Module EasyTicket (Étiquettes)
✅ Génération d'étiquettes d'expédition format A6 (100×150mm)  
✅ Support de multiples transporteurs (Colissimo, Chronopost, Mondial Relay, UPS, DPD)  
✅ Pictogrammes visuels (fragile, assuré, signature obligatoire)  
✅ Numéro de suivi et code-barres  
✅ Gestion du contenu du colis avec valorisation  
✅ Instructions de livraison personnalisées  
✅ Design optimisé pour impression thermique ou A4  

### 🔗 Intégration entre modules
✅ **Passage automatique des données** : Après génération d'une étiquette, possibilité de créer la facture correspondante sans ressaisie  
✅ **Historique** : Les étiquettes et factures sont liées en base de données  
✅ Navigation fluide entre les deux modules  

---

## 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| **Framework** | Django 5.x |
| **Base de données** | SQLite (développement) / PostgreSQL (production) |
| **Génération PDF** | WeasyPrint |
| **Interactions dynamiques** | HTMX |
| **Styles** | Bootstrap 5 + CSS personnalisé |
| **Polices système** | Arial, Helvetica (pour performance) |
| **Hébergement** | PythonAnywhere |

---

## 📦 Installation

### Prérequis
- Python 3.10+
- pip
- virtualenv (recommandé)

### 1. Cloner le projet
```bash
git clone <votre-repo>
cd EasInvoice
```

### 2. Créer un environnement virtuel
```bash
python -m venv easy_env
# Windows
easy_env\Scripts\activate
# Linux/Mac
source easy_env/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration
Créer un fichier `.env` à la racine :
```env
SECRET_KEY=votre-clé-secrète-django
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Créer un superutilisateur (optionnel)
```bash
python manage.py createsuperuser
```

### 7. Lancer le serveur
```bash
python manage.py runserver
```

Accéder à l'application :
- **Factures** : http://127.0.0.1:8000/
- **Étiquettes** : http://127.0.0.1:8000/etiquette/
- **Admin** : http://127.0.0.1:8000/admin/

---

## 📖 Utilisation

### Générer une étiquette puis une facture (workflow complet)

1. **Créer une étiquette**
   - Aller sur http://127.0.0.1:8000/etiquette/
   - Remplir les informations :
     - Expéditeur (votre entreprise)
     - Destinataire (client)
     - Informations du colis (poids, dimensions)
     - Contenu du colis (articles avec quantités et valeurs)
   - Cliquer sur "Générer l'étiquette PDF"
   - Le PDF est téléchargé automatiquement

2. **Générer la facture correspondante**
   - Un message de succès s'affiche avec le bouton "Générer la facture"
   - Cliquer sur ce bouton
   - Le formulaire de facture est **pré-rempli** avec les données de l'étiquette :
     - Expéditeur → Émetteur
     - Destinataire → Client
     - Articles du colis → Lignes de facture
     - Numéro de commande → Numéro de facture
   - Compléter les champs manquants :
     - SIRET, RCS (si applicable)
     - Taux de TVA ou franchise
     - Conditions de paiement
     - Date d'échéance
   - Cliquer sur "Générer la facture PDF"
   - Le PDF de facture est téléchargé

3. **Résultat**
   - Vous avez maintenant :
     - ✅ Une étiquette d'expédition professionnelle
     - ✅ Une facture conforme à la législation française
     - ✅ Les deux documents sont liés en base de données

---

## 🎨 Personnalisation

### Couleurs du thème
Modifier les variables CSS dans `templates/CORE/form.html` et `templates/TICKET/ticket_form.html` :
```css
:root {
    --primary-blue: #1e3a8a;
    --accent-green: #10b981;
    --light-bg: #f8fafc;
}
```

### Logo
Remplacer le fichier `static/CORE/img/easyLogo.png` par votre propre logo.

### Mentions légales de la facture
Modifier `templates/CORE/invoice.html` pour ajuster le design du PDF.

### Design de l'étiquette
Modifier `templates/TICKET/ticket_label.html` et `static/TICKET/css/label.css`.

---

## 🔧 Configuration avancée

### Utiliser PostgreSQL en production
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'easyinvoice_db',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Activer le nettoyage automatique des données (RGPD)
Créer un script de nettoyage dans `utils/cleanup.py` :
```python
from django.utils import timezone
from datetime import timedelta
from TICKET.models import Ticket
from CORE.models import Invoice

def cleanup_old_data():
    """Supprimer les données de plus de 30 jours"""
    cutoff_date = timezone.now() - timedelta(days=30)
    
    Ticket.objects.filter(created_at__lt=cutoff_date).delete()
    Invoice.objects.filter(created_at__lt=cutoff_date).delete()
```

Ajouter une tâche cron (avec django-crontab) :
```python
# settings.py
CRONJOBS = [
    ('0 2 * * *', 'utils.cleanup.cleanup_old_data')  # Tous les jours à 2h
]
```

---

## 🚀 Déploiement sur PythonAnywhere

### 1. Créer un compte PythonAnywhere
Aller sur https://www.pythonanywhere.com/

### 2. Uploader le code
```bash
git clone <votre-repo> ~/EasInvoice
cd ~/EasInvoice
```

### 3. Installer les dépendances
```bash
mkvirtualenv --python=/usr/bin/python3.10 easy_env
pip install -r requirements.txt
```

### 4. Configuration
Créer un fichier `.env` avec les variables de production.

### 5. Configurer l'application web
Dans l'interface PythonAnywhere :
- **Source code** : `/home/votre_username/EasInvoice`
- **Working directory** : `/home/votre_username/EasInvoice`
- **Virtualenv** : `/home/votre_username/.virtualenvs/easy_env`
- **WSGI file** : Modifier pour pointer vers `EasInvoice.wsgi`

### 6. Migrations et static
```bash
python manage.py migrate
python manage.py collectstatic
```

### 7. Recharger l'application
Cliquer sur "Reload" dans l'interface PythonAnywhere.

---

## 📊 Structure du projet

```
EasInvoice/
│
├── CORE/                       # Module Factures
│   ├── migrations/
│   ├── models.py              # Modèles Invoice, InvoiceItem
│   ├── views.py               # Génération de factures
│   ├── forms.py               # Formulaires de saisie
│   ├── urls.py
│   └── admin.py
│
├── TICKET/                     # Module Étiquettes
│   ├── migrations/
│   ├── models.py              # Modèles Ticket, TicketItem
│   ├── views.py               # Génération d'étiquettes
│   ├── forms.py               # Formulaires de saisie
│   ├── urls.py
│   └── admin.py
│
├── templates/
│   ├── CORE/
│   │   ├── form.html          # Formulaire de facture
│   │   ├── invoice.html       # Template PDF facture
│   │   ├── _item_row.html     # Ligne d'article (HTMX)
│   │   └── privacy_policy.html
│   └── TICKET/
│       ├── ticket_form.html   # Formulaire d'étiquette
│       ├── ticket_label.html  # Template PDF étiquette
│       └── _package_item.html # Ligne d'article (HTMX)
│
├── static/
│   ├── CORE/
│   │   └── css/
│   │       └── invoice.css    # Styles facture PDF
│   └── TICKET/
│       └── css/
│           └── label.css      # Styles étiquette PDF
│
├── EasInvoice/                # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🔐 Sécurité et conformité

### RGPD
- ✅ **Pas de cookies tiers** : Aucun tracking
- ✅ **Traitement en mémoire** : Les données sont traitées puis supprimées
- ✅ **Base de données temporaire** : Option de nettoyage automatique après 30 jours
- ✅ **HTTPS obligatoire** en production
- ✅ **Politique de confidentialité** détaillée accessible sur le site

### Conformité légale française
- ✅ Mentions obligatoires sur les factures (SIRET, RCS, TVA, etc.)
- ✅ Support de la franchise de TVA (art. 293 B du CGI)
- ✅ Pénalités de retard et indemnité forfaitaire de recouvrement
- ✅ Mention autoliquidation (BTP)
- ✅ Numérotation séquentielle des factures

---

## 🐛 Résolution de problèmes

### WeasyPrint ne s'installe pas (Windows)
WeasyPrint nécessite GTK+ sur Windows. Solutions :
1. Utiliser WSL2 (recommandé)
2. Installer GTK+ manuellement
3. Utiliser Docker

### PDF trop lent à générer
- ✅ Utiliser des polices système (Arial) plutôt que des TTF
- ✅ Définir `base_url=None` dans WeasyPrint
- ✅ Éviter les images lourdes
- ✅ Simplifier le CSS

### Erreur de migration
```bash
# Réinitialiser les migrations
python manage.py migrate --fake CORE zero
python manage.py migrate --fake TICKET zero
python manage.py makemigrations
python manage.py migrate
```

---

## 🎯 Roadmap

### Version actuelle (v1.0)
- ✅ Génération de factures PDF
- ✅ Génération d'étiquettes d'expédition
- ✅ Intégration entre les deux modules
- ✅ Base de données SQLite
- ✅ Interface responsive

### Futures évolutions (v2.0 - Premium)
- 🔜 Génération en masse (CSV import)
- 🔜 Intégration API transporteurs (Colissimo, Chronopost)
- 🔜 Codes-barres automatiques via API
- 🔜 Historique et recherche avancée
- 🔜 Modèles personnalisables (logos, couleurs)
- 🔜 Export multi-formats (PNG, JPEG)
- 🔜 Calcul automatique des frais de port
- 🔜 Impression directe (sans téléchargement)
- 🔜 Multi-utilisateurs avec comptes
- 🔜 Tableau de bord avec statistiques

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👨‍💻 Auteur

Développé avec ❤️ pour simplifier la vie des entrepreneurs et freelances.

---

## 📞 Support

Pour toute question ou problème :
- 📧 Email : support@easyinvoice.fr
- 🌐 Site web : https://easyinvoice.fr
- 📚 Documentation : Voir ce README

---

## 🙏 Remerciements

- Django pour le framework puissant
- WeasyPrint pour la génération PDF
- Bootstrap pour le design responsive
- HTMX pour les interactions dynamiques
- La communauté open source

---

**EasyInvoice** - Factures et étiquettes professionnelles en quelques clics ! 🚀

