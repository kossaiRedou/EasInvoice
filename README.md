# 🧾 EasyInvoice — Documentation

EasyInvoice est une application Django permettant de générer des factures PDF professionnelles à partir d’un formulaire simple, sans base de données. L’interface est moderne, les lignes d’articles sont dynamiques (HTMX), et l’architecture est prête pour une future version « premium ».

## ✨ Fonctionnalités

- Formulaire complet côté émetteur et destinataire (nom/entreprise, adresse, ville, email, EI, SIRET, RCS)
- Lignes d’articles dynamiques (ajout/suppression) via HTMX et formset Django
- Calculs automatiques des totaux (HT, TVA, TTC) avec prise en charge de la franchise de TVA (art. 293 B CGI)
- Mentions conformes: EI, SIRET/RCS, autoliquidation (option), pénalités de retard, indemnité de recouvrement (40 €)
- Rendu imprimable stylé (CSS) + noms en majuscules (affichage)
- Génération PDF avec WeasyPrint (si installé)

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

3) Démarrer
```bash
python manage.py runserver
```

4) Ouvrir
```
http://127.0.0.1:8000/
```

## 🧠 Utilisation

1. Renseignez les infos émetteur/destinataire (ville et email inclus). Cochez « Entrepreneur Individuel » si applicable.
2. Ajoutez vos articles (+ Ajouter une ligne). Supprimez-en si besoin.
3. Choisissez vos dates (émission, prestation, échéance).
4. Définissez TVA (ou cochez la franchise).
5. Optionnel: modalités de paiement, pénalités, recouvrement, autoliquidation.
6. Cliquez « Générer la facture PDF ».

Si WeasyPrint est absent, installez-le pour produire un PDF. Sous Windows, suivez la doc WeasyPrint (GTK runtime).

## 🧩 Détails techniques

- HTMX + formset: `add-item-row/` renvoie un formulaire vide avec index incrémenté et champ `DELETE` prêt; suppression visuelle coche `DELETE`.
- Conformité: mentions EI (badge), SIRET/RCS, 293 B CGI, autoliquidation, pénalités et recouvrement.
- Mise en page: sections « Émetteur » et « Destinataire » compactes; noms en MAJUSCULES avec `.company-name`.

## 🔧 Personnalisation

- Styles: `static/CORE/css/invoice.css`
- Template facture: `templates/CORE/invoice.html`
- Ajouter un logo: placer dans `static/CORE/images/` et l’intégrer au template

## 🔮 Évolutions (premium)

- Multi-modèles, logo, remises/acompte, prévisualisation HTML, historique, exports, QR code, paiements

## 🛟 Dépannage

- PDF absent: installer WeasyPrint + dépendances système
- Articles manquants: vérifier que les champs requis sont remplis et que la ligne n’est pas marquée `DELETE`

---

Made by EasyInvoice
