# 🧾 EasyInvoice — Documentation

EasyInvoice est une application Django complète permettant de **générer, sauvegarder et gérer des factures PDF professionnelles** avec système d'authentification, historique complet et gestion des clients. L'interface est moderne, les lignes d'articles sont dynamiques (HTMX), et toutes les données sont persistées en base de données.

## ✨ Fonctionnalités

### 🔐 Gestion des utilisateurs
- Inscription et connexion sécurisées
- Profil utilisateur avec informations de facturation (pré-remplissage automatique)
- Dashboard personnalisé avec statistiques en temps réel

### 📄 Création de factures
- Formulaire complet côté émetteur et destinataire (nom/entreprise, adresse, ville, email, EI, SIRET, RCS)
- Lignes d'articles dynamiques (ajout/suppression) via HTMX et formset Django
- Calculs automatiques des totaux (HT, TVA, TTC) avec prise en charge de la franchise de TVA (art. 293 B CGI)
- Mentions conformes: EI, SIRET/RCS, autoliquidation (option), pénalités de retard, indemnité de recouvrement (40 €)
- Génération PDF avec WeasyPrint

### 💾 Historique et suivi
- Sauvegarde automatique de toutes les factures en base de données
- Historique complet avec recherche et filtres
- Gestion des statuts : Brouillon, Envoyée, Payée, En retard, Annulée
- Téléchargement PDF à tout moment depuis l'historique
- Vue détaillée de chaque facture

### 👥 Gestion des clients
- Enregistrement des clients récurrents
- Pré-remplissage rapide lors de la création de factures
- Historique des factures par client

### 📊 Dashboard et statistiques
- Total des factures
- Montant des revenus (factures payées)
- Montant en attente
- Factures en retard
- Vue d'ensemble rapide des dernières factures

## 📁 Structure du projet

```
EasInvoice/
├── CORE/
│   ├── forms.py              # Formulaire principal + ItemForm
│   ├── views.py              # Logique: form + formset + PDF
│   ├── urls.py               # Routes: '/' + 'add-item-row/' (HTMX)
│   └── templates/CORE/
│       ├── form.html         # UI du formulaire (Bootstrap + HTMX)
│       ├── _item_row.html    # Partial HTMX pour une ligne article
│       └── invoice.html      # Template de facture imprimable
├── static/CORE/css/invoice.css # Styles d’impression et mise en forme
├── EasInvoice/               # Config Django
│   ├── settings.py
│   └── urls.py
├── requirements.txt          # Dépendances Python
├── Procfile                  # Déploiement (ex. Render)
└── manage.py
```

## 🚀 Installation & Lancement

1) Créer et activer un venv
```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate
```

2) Installer les dépendances
```bash
pip install -r requirements.txt
```

3) **[IMPORTANT]** Créer les tables de base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

4) Créer un compte administrateur (optionnel)
```bash
python manage.py createsuperuser
```

5) Démarrer le serveur
```bash
python manage.py runserver
```

6) Ouvrir dans votre navigateur
```
http://127.0.0.1:8000/
```

7) Créer un compte utilisateur via l'interface web ou utiliser le compte admin

## 🧠 Utilisation

### Première utilisation :
1. Accédez à la page d'accueil : `http://127.0.0.1:8000/`
2. Cliquez sur "Créer un compte" et inscrivez-vous
3. Vous serez automatiquement redirigé vers votre dashboard

### Créer une facture :
1. Depuis le dashboard, cliquez sur "Nouvelle facture"
2. Vos informations d'émetteur sont pré-remplies (modifiables)
3. Renseignez les infos du client
4. Ajoutez vos articles (+ Ajouter une ligne)
5. Définissez les dates, TVA et conditions de paiement
6. Cliquez sur "Générer la facture PDF"
7. La facture est **automatiquement sauvegardée** et le PDF se télécharge

### Gérer vos factures :
- **Liste** : Consultez toutes vos factures dans "Mes factures"
- **Détails** : Cliquez sur "Voir" pour afficher les détails complets
- **Statut** : Changez le statut (Brouillon → Envoyée → Payée)
- **PDF** : Téléchargez à nouveau le PDF à tout moment
- **Suppression** : Supprimez une facture si nécessaire

### Gérer vos clients :
- Allez dans "Clients" pour ajouter des clients récurrents
- Utilisez-les pour pré-remplir rapidement vos prochaines factures

**Note:** Si WeasyPrint est absent, installez-le pour produire un PDF. Sous Windows, suivez la doc WeasyPrint (GTK runtime).

## 🧩 Détails techniques

- HTMX + formset: `add-item-row/` renvoie un formulaire vide avec index incrémenté et champ `DELETE` prêt; suppression visuelle coche `DELETE`.
- Conformité: mentions EI (badge), SIRET/RCS, 293 B CGI, autoliquidation, pénalités et recouvrement.
- Mise en page: sections « Émetteur » et « Destinataire » compactes; noms en MAJUSCULES avec `.company-name`.

## 🔧 Personnalisation

- Styles: `static/CORE/css/invoice.css`
- Template facture: `templates/CORE/invoice.html`
- Ajouter un logo: placer dans `static/CORE/images/` et l’intégrer au template

## 🔮 Évolutions futures possibles

Fonctionnalités déjà implémentées :
- ✅ Historique des factures
- ✅ Gestion des clients
- ✅ Système d'authentification
- ✅ Dashboard avec statistiques
- ✅ Gestion des états de factures

Améliorations possibles :
- Multi-modèles de factures (templates personnalisables)
- Upload de logo personnalisé
- Remises et acomptes
- Prévisualisation HTML avant génération
- Exports Excel/CSV
- QR code pour paiement
- Intégration de paiements en ligne
- Envoi automatique par email
- Rappels automatiques pour factures en retard
- Multi-devises

## 🛟 Dépannage

### Erreurs courantes :

**"no such table: CORE_invoice"**
→ Vous n'avez pas exécuté les migrations. Lancez :
```bash
python manage.py makemigrations
python manage.py migrate
```

**PDF absent / Erreur WeasyPrint**
→ Installer WeasyPrint + dépendances système :
```bash
pip install weasyprint
```
Sous Windows, suivez la documentation officielle pour installer GTK.

**Articles manquants dans la facture**
→ Vérifier que les champs requis sont remplis et que la ligne n'est pas marquée `DELETE`

**Impossible de me connecter**
→ Vérifiez que vous avez créé un compte via `/register/` ou utilisez le compte superuser

**Mes informations ne sont pas pré-remplies**
→ Créez d'abord une facture complète, ou renseignez votre profil via l'admin Django

**Erreur 404 sur les anciennes URLs**
→ Les URLs ont changé. Utilisez `/dashboard/` au lieu de `/` pour accéder à l'application après connexion

---

Made with ❤️ by EasyInvoice
