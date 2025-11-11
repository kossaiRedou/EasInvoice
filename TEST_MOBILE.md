# 📱 Checklist de Test Mobile - EasyInvoice

## 🎯 Comment tester l'application sur mobile

### Méthode 1 : Via Chrome DevTools (Simulation)

1. **Ouvrir Chrome DevTools** : Appuyez sur `F12`
2. **Activer le mode mobile** : Cliquez sur l'icône 📱 ou `Ctrl+Shift+M`
3. **Sélectionner un appareil** : iPhone 12 Pro, Galaxy S20, etc.
4. **Tester toutes les pages** en suivant la checklist ci-dessous

### Méthode 2 : Sur un vrai téléphone (Recommandé)

1. **Démarrer le serveur** sur votre PC :
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Trouver l'IP de votre PC** :
   - Windows : `ipconfig` → Chercher "Adresse IPv4"
   - Mac/Linux : `ifconfig` → Chercher "inet"
   - Exemple : `192.168.1.10`

3. **Connecter votre téléphone** au même WiFi que votre PC

4. **Ouvrir le navigateur mobile** et aller à :
   ```
   http://VOTRE_IP:8000
   ```
   Exemple : `http://192.168.1.10:8000`

---

## ✅ Checklist de Test

### 📊 **Dashboard** (`/dashboard/`)

**Layout et Design**
- [ ] Les 4 cartes statistiques s'affichent en 2 colonnes sur mobile
- [ ] Les montants sont lisibles
- [ ] Le bouton "Créer une nouvelle facture" est en pleine largeur
- [ ] La table des dernières factures est scrollable horizontalement
- [ ] Les colonnes "Date" et "Actions" sont masquées sur très petit écran

**Navigation**
- [ ] Le bouton menu hamburger (☰) est visible en haut à gauche
- [ ] Un tap sur le menu ouvre le sidebar
- [ ] Un tap sur l'overlay ferme le sidebar
- [ ] Le menu reste accessible après navigation

**Touch Targets**
- [ ] Tous les boutons sont facilement cliquables (pas trop petits)
- [ ] Les liens dans la table sont faciles à taper

---

### 📝 **Formulaire de création de facture** (`/invoice/create/`)

**Layout Responsive**
- [ ] Le formulaire s'affiche en une colonne
- [ ] Les sections (Émetteur, Destinataire, etc.) sont empilées verticalement
- [ ] Les champs prennent toute la largeur
- [ ] Le padding des cards est réduit mais l'interface reste aérée

**Champs de saisie**
- [ ] Les inputs ont une taille minimale de 44px
- [ ] Le clavier ne zoom pas automatiquement sur iOS lors du focus
- [ ] Les champs date/select sont facilement utilisables
- [ ] Les textarea sont scrollables

**Bouton d'action**
- [ ] Le bouton "Créer la facture" reste visible en bas (sticky)
- [ ] Le bouton a une bonne taille (facile à taper)
- [ ] Un tap sur le bouton soumet bien le formulaire

**Gestion des items**
- [ ] Le bouton "Ajouter une ligne" est bien visible (min 50px)
- [ ] Les lignes d'items s'empilent verticalement
- [ ] Le bouton supprimer est accessible

---

### 📄 **Détail de facture** (`/invoice/ID/`)

**Header et Actions**
- [ ] Les boutons "Télécharger PDF" et "Retour" sont empilés verticalement
- [ ] Les boutons sont en pleine largeur
- [ ] Les boutons sont facilement cliquables

**Informations**
- [ ] Les cartes d'infos s'affichent bien
- [ ] Les info-boxes sont compactes mais lisibles
- [ ] Le layout est en une colonne (col-lg-8 puis col-lg-4)

**Table des articles**
- [ ] La table est scrollable horizontalement
- [ ] La colonne "Quantité" est masquée sur très petit écran
- [ ] Les montants restent visibles et alignés

**Sidebar d'actions**
- [ ] Le formulaire de changement de statut est utilisable
- [ ] Le select est facilement tapable
- [ ] Les boutons "Mettre à jour" et "Supprimer" sont en pleine largeur

---

### 📋 **Liste des factures** (`/invoices/`)

**Layout**
- [ ] Le bouton "Nouvelle facture" est en pleine largeur
- [ ] La table s'affiche correctement

**Table responsive**
- [ ] Sur mobile (< 768px) : table compacte mais lisible
- [ ] Sur petit écran (< 576px) : colonnes Date émission et Échéance masquées
- [ ] Scroll horizontal fonctionne bien
- [ ] Les badges de statut sont visibles

**Actions**
- [ ] Les boutons d'actions (Voir, Télécharger) sont cliquables
- [ ] Pas de chevauchement entre boutons

---

### 👥 **Liste des clients** (`/clients/`)

**Layout**
- [ ] Le bouton "Ajouter un client" est en pleine largeur
- [ ] La table est responsive

**Table**
- [ ] Sur très petit écran : seul le nom et actions sont visibles
- [ ] Colonnes email, téléphone, ville masquées sur mobile
- [ ] Scroll horizontal fonctionne

---

### 👤 **Profil utilisateur** (`/profile/edit/`)

**Formulaire**
- [ ] Tous les champs sont en pleine largeur
- [ ] Les champs sont facilement éditables
- [ ] Les labels sont clairs

**Boutons d'action**
- [ ] Les boutons "Enregistrer" et "Annuler" sont empilés verticalement
- [ ] Les boutons sont en pleine largeur
- [ ] Les boutons sont facilement tapables

**Sidebar info**
- [ ] Les cartes d'info s'affichent en dessous du formulaire sur mobile

---

### 🎨 **Menu Sidebar** (Toutes les pages)

**Fonctionnement**
- [ ] Le bouton hamburger est toujours visible (50x50px)
- [ ] Le bouton a une bonne couleur et ombre
- [ ] Un tap ouvre le sidebar depuis la gauche
- [ ] Un tap sur l'overlay ferme le sidebar
- [ ] L'overlay a un effet de blur

**Contenu du menu**
- [ ] Le logo "EasInvoice" est visible
- [ ] Les liens de navigation sont espacés
- [ ] Les icônes sont alignées
- [ ] La section profil utilisateur en bas est visible
- [ ] Le lien de déconnexion est accessible

**Responsive**
- [ ] Sur desktop, le sidebar est fixe (pas de hamburger)
- [ ] Sur mobile, le sidebar se cache par défaut
- [ ] Le sidebar ne cache pas le contenu sur desktop

---

## 🧪 Tests d'interaction tactile

### Test 1 : Création rapide d'une facture
1. Ouvrir le menu → Cliquer "Créer une facture"
2. Remplir le formulaire avec seulement le minimum
3. Ajouter 2-3 lignes d'items
4. Scroller vers le bas
5. Le bouton "Créer" doit rester visible (sticky)
6. Soumettre le formulaire
7. Redirection vers la page de détail

### Test 2 : Navigation rapide
1. Ouvrir le menu hamburger
2. Aller au Dashboard
3. Ouvrir le menu à nouveau
4. Aller à "Mes factures"
5. Sélectionner une facture
6. Télécharger le PDF
7. Retour à la liste

### Test 3 : Édition du profil
1. Ouvrir le menu
2. Cliquer sur la section utilisateur (en bas)
3. Modifier les informations
4. Taper "Enregistrer"
5. Vérifier le message de succès

---

## ⚠️ Points d'attention

### À vérifier spécialement

1. **Zoom automatique sur iOS** :
   - Taper dans un input ne doit PAS zoomer la page
   - Si ça zoom, vérifier que font-size est bien ≥ 16px

2. **Touch targets** :
   - Tous les boutons doivent faire minimum 44x44px
   - Pas de boutons trop proches les uns des autres

3. **Scroll horizontal des tables** :
   - Le scroll doit être fluide (momentum scrolling)
   - Pas de scroll "coincé"

4. **Menu sidebar** :
   - L'overlay doit bloquer les interactions avec le contenu
   - Le menu doit se fermer au tap sur l'overlay

5. **Formulaires** :
   - Les selects doivent ouvrir le picker natif
   - Les inputs date doivent ouvrir le picker natif
   - Pas de problème de focus

---

## 🐛 Bugs connus / Limitations

### iOS Safari
- [ ] Vérifier que les inputs type="date" fonctionnent
- [ ] Vérifier que le sticky button fonctionne correctement

### Android Chrome
- [ ] Vérifier le comportement du menu hamburger
- [ ] Vérifier les transitions du sidebar

### Petit écran (< 375px)
- [ ] Certains textes peuvent nécessiter un scroll horizontal

---

## 📈 Résultats attendus

Après tous ces tests, l'application doit être :
- ✅ Entièrement utilisable sur mobile
- ✅ Navigation fluide et intuitive
- ✅ Tous les boutons facilement tapables
- ✅ Formulaire de facture remplissable confortablement
- ✅ Tables lisibles avec scroll horizontal
- ✅ Aucun zoom automatique intempestif

---

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifier la taille de l'écran testée (DevTools)
2. Vider le cache du navigateur (Ctrl+Shift+R)
3. Vérifier que tous les fichiers CSS sont bien chargés
4. Consulter la console du navigateur pour les erreurs

**Bon test ! 🚀**

