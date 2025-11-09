# 🚀 Guide de Démarrage - EasyInvoice avec Base de Données

## ✅ Ce qui a été ajouté

Votre application EasyInvoice a été transformée en une **application complète avec gestion de comptes utilisateurs** :

### Nouvelles fonctionnalités :
- ✅ **Système d'authentification** : Inscription, connexion, déconnexion
- ✅ **Profil utilisateur** : Informations sauvegardées automatiquement
- ✅ **Sauvegarde des factures** : Toutes vos factures sont conservées en base de données
- ✅ **Historique complet** : Consultez toutes vos factures passées
- ✅ **Gestion des statuts** : Brouillon, Envoyée, Payée, En retard, Annulée
- ✅ **Dashboard avec statistiques** : Vue d'ensemble de votre activité
- ✅ **Gestion des clients** : Enregistrez vos clients récurrents
- ✅ **Téléchargement PDF** : Générez le PDF de n'importe quelle facture enregistrée

---

## 📋 Étapes d'installation

### 1. Créer les tables de base de données (MIGRATIONS)

La première chose à faire est de créer les nouvelles tables dans votre base de données :

```bash
# Créer les fichiers de migration
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate
```

### 2. Créer un compte administrateur (optionnel mais recommandé)

Pour accéder à l'interface d'administration Django :

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer votre compte admin.

### 3. Lancer le serveur

```bash
python manage.py runserver
```

### 4. Tester l'application

Ouvrez votre navigateur et accédez à : `http://127.0.0.1:8000/`

---

## 🎯 Flux d'utilisation

### Pour les nouveaux utilisateurs :

1. **Page d'accueil** (`/`) → Présentation du service
2. **Inscription** (`/register/`) → Créer un compte
3. **Dashboard** (`/dashboard/`) → Vue d'ensemble automatique après inscription
4. **Créer une facture** (`/invoice/new/`) → Formulaire de facture (vos infos sont pré-remplies !)
5. **Historique** (`/invoice/`) → Liste de toutes vos factures

### Actions disponibles :

- **Voir une facture** : Détails complets avec tous les montants
- **Télécharger en PDF** : Générer le PDF à tout moment
- **Changer le statut** : Passer de "Brouillon" à "Envoyée" puis "Payée"
- **Supprimer une facture** : Avec confirmation de sécurité
- **Gérer des clients** : Ajouter des clients récurrents

---

## 🗂️ Structure de la Base de Données

### Tables créées :

1. **UserProfile** : Profil étendu de l'utilisateur
   - Nom de l'entreprise
   - Adresse, ville, email
   - SIRET, RCS
   - Statut Entrepreneur Individuel

2. **Client** : Clients récurrents
   - Nom, adresse, ville
   - Email, téléphone
   - Notes

3. **Invoice** : Factures
   - Toutes les informations émetteur/destinataire
   - Dates (émission, prestation, échéance)
   - Montants (HT, TVA, TTC)
   - Statut (draft, sent, paid, overdue, cancelled)
   - Conditions de paiement

4. **InvoiceItem** : Lignes d'articles
   - Description, quantité, prix unitaire
   - Total ligne

---

## 🔧 Configuration

### Variables d'environnement (.env)

Assurez-vous que votre fichier `.env` contient :

```env
SECRET_KEY=votre-clé-secrète-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Paramètres d'authentification

Les paramètres suivants ont été ajoutés dans `settings.py` :

```python
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
```

---

## 📊 Interface d'administration

Accédez à l'interface d'administration Django : `http://127.0.0.1:8000/admin/`

Vous pourrez gérer :
- Utilisateurs et profils
- Clients
- Factures et leurs articles
- Modifier les statuts directement

---

## 🎨 Pages disponibles

| URL | Description | Authentification requise |
|-----|-------------|-------------------------|
| `/` | Page d'accueil publique | Non |
| `/register/` | Inscription | Non |
| `/login/` | Connexion | Non |
| `/logout/` | Déconnexion | Oui |
| `/dashboard/` | Tableau de bord | Oui |
| `/invoice/new/` | Nouvelle facture | Oui |
| `/invoice/` | Liste des factures | Oui |
| `/invoice/<id>/` | Détail d'une facture | Oui |
| `/invoice/<id>/pdf/` | Télécharger PDF | Oui |
| `/clients/` | Liste des clients | Oui |
| `/clients/new/` | Ajouter un client | Oui |
| `/privacy-policy/` | Politique de confidentialité | Non |

---

## 🐛 Dépannage

### Erreur "no such table"
→ Vous n'avez pas exécuté les migrations. Lancez :
```bash
python manage.py migrate
```

### Les informations de l'émetteur ne sont pas pré-remplies
→ Votre profil utilisateur est vide. Remplissez-le via l'admin ou en créant votre première facture.

### Erreur WeasyPrint
→ WeasyPrint doit être installé pour générer les PDF :
```bash
pip install weasyprint
```

Sous Windows, suivez la documentation officielle pour installer GTK.

### Je ne peux pas me connecter
→ Vérifiez que vous avez bien créé un compte via `/register/`

---

## 🔄 Migration depuis l'ancienne version

Si vous aviez l'ancienne version sans base de données :

1. Les factures créées avant ne sont **pas sauvegardées** (c'était le comportement normal)
2. Toutes les nouvelles factures créées après les migrations seront **automatiquement sauvegardées**
3. Vous devez créer un compte pour utiliser les nouvelles fonctionnalités

---

## 📈 Prochaines étapes recommandées

1. **Complétez votre profil utilisateur** via l'admin
2. **Ajoutez quelques clients** récurrents
3. **Créez votre première facture** et testez le workflow complet
4. **Explorez le dashboard** pour voir les statistiques

---

## 🛡️ Sécurité

- Les utilisateurs ne peuvent voir que **leurs propres factures**
- Toutes les vues de gestion sont **protégées par authentification**
- Les mots de passe sont **hashés** par Django
- Les tokens CSRF sont **activés** sur tous les formulaires

---

## 📞 Support

En cas de problème :
- Consultez les logs Django dans la console
- Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`
- Assurez-vous que les migrations sont appliquées : `python manage.py showmigrations`

---

**Bon travail avec votre nouvelle application EasyInvoice ! 🎉**

