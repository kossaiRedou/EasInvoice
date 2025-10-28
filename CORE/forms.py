from django import forms


class InvoiceForm(forms.Form):
    """Formulaire pour créer une facture simple"""
    
    # Informations de l'émetteur
    from_name = forms.CharField(
        label='Nom/Entreprise',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom ou entreprise'
        })
    )
    
    from_address = forms.CharField(
        label='Adresse',
        max_length=200,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'N°, rue, code postal'
        })
    )

    from_city = forms.CharField(
        label='Ville',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville, Pays/Région'})
    )

    from_email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@domaine.com'})
    )
    
    siret = forms.CharField(
        label='SIRET (optionnel)',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 123 456 789 00012'
        })
    )
    
    rcs = forms.CharField(
        label='RCS / Immatriculation (optionnel)',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: RCS Paris 123 456 789'
        })
    )

    is_ei = forms.BooleanField(
        label='Entrepreneur Individuel (EI)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    # Informations du client
    to_name = forms.CharField(
        label='Nom/Entreprise client',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom du client'
        })
    )
    
    to_address = forms.CharField(
        label='Adresse',
        max_length=200,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'N°, rue, code postal'
        })
    )

    to_city = forms.CharField(
        label='Ville',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville, Pays/Région'})
    )

    to_email = forms.EmailField(
        label='Email',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@domaine.com'})
    )
    
    # Informations de la facture
    invoice_number = forms.CharField(
        label='Numéro de facture',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: FACT-001'
        })
    )
    
    invoice_date = forms.DateField(
        label='Date d\'émission',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    service_date_start = forms.DateField(
        label='Début de la prestation',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    service_date_end = forms.DateField(
        label='Fin de la prestation',
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    due_date = forms.DateField(
        label='Date d\'échéance',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    # Anciens champs d'une seule ligne (compatibilité)
    description = forms.CharField(
        label='Description du produit/service (simple)',
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Description détaillée'
        })
    )
    
    quantity = forms.DecimalField(
        label='Quantité (simple)',
        max_digits=10,
        decimal_places=2,
        required=False,
        initial=1.00,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    unit_price = forms.DecimalField(
        label='Prix unitaire HT (simple)',
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )
    
    is_vat_exempt = forms.BooleanField(
        label='Franchise de TVA (art. 293 B CGI)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    vat_rate = forms.DecimalField(
        label='Taux de TVA (%)',
        max_digits=5,
        decimal_places=2,
        required=False,
        initial=20.00,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01'
        })
    )

    # Conditions de paiement
    payment_terms = forms.CharField(
        label='Modalités de paiement (optionnel)',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 2,
            'placeholder': 'Ex: Virement sous 30 jours'
        })
    )

    late_fee_rate = forms.DecimalField(
        label='Taux pénalités de retard (%)',
        max_digits=5,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Ex: 10.00'
        })
    )

    recovery_fee = forms.BooleanField(
        label='Indemnité forfaitaire de recouvrement (40€)',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    autoliquidation = forms.BooleanField(
        label='Autoliquidation (BTP / cas particuliers)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )


class ItemForm(forms.Form):
    description = forms.CharField(
        label='Description', max_length=500, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Désignation'}))
    quantity = forms.DecimalField(
        label='Qté', max_digits=10, decimal_places=2, required=True,
        initial=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    unit_price = forms.DecimalField(
        label='PU HT', max_digits=10, decimal_places=2, required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
