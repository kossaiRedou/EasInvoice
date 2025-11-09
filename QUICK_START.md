# ⚡ Démarrage Rapide - EasyInvoice

## 🎯 En 3 commandes

```bash
# 1. Créer la base de données
python manage.py makemigrations
python manage.py migrate

# 2. Créer un admin (optionnel)
python manage.py createsuperuser

# 3. Lancer l'application
python manage.py runserver
```

Puis ouvrez : **http://127.0.0.1:8000/**

---

## 📱 Utilisation en 4 étapes

1. **Inscription** : Cliquez sur "Créer un compte"
2. **Dashboard** : Vous êtes redirigé automatiquement
3. **Nouvelle facture** : Cliquez sur le bouton bleu
4. **Remplissez et validez** : Votre facture est sauvegardée et le PDF se télécharge

---

## 🗺️ Navigation

| Page | URL | Description |
|------|-----|-------------|
| Accueil | `/` | Page publique |
| Connexion | `/login/` | Se connecter |
| Inscription | `/register/` | Créer un compte |
| Dashboard | `/dashboard/` | Vue d'ensemble |
| Nouvelle facture | `/invoice/new/` | Créer une facture |
| Mes factures | `/invoice/` | Historique |
| Clients | `/clients/` | Gérer les clients |
| Admin | `/admin/` | Administration Django |

---

## ✅ Statuts des factures

- **Brouillon** : Facture en cours de création
- **Envoyée** : Facture transmise au client
- **Payée** : Paiement reçu ✓
- **En retard** : Échéance dépassée ⚠️
- **Annulée** : Facture annulée

---

## 🆘 Problème ?

**Erreur "no such table"**
```bash
python manage.py migrate
```

**PDF ne se génère pas**
```bash
pip install weasyprint
```

**Impossible de se connecter**
- Créez un compte via `/register/`
- Ou utilisez le compte superuser

---

## 📚 Plus d'infos

- **README.md** : Documentation complète
- **GUIDE_DEMARRAGE.md** : Guide détaillé
- **CHANGELOG.md** : Liste des fonctionnalités

---

**C'est parti ! 🚀**

