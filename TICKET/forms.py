from django import forms
from django.forms import formset_factory
from .models import Ticket, TicketItem
from datetime import date


class TicketForm(forms.ModelForm):
    """Formulaire pour créer une étiquette"""
    
    class Meta:
        model = Ticket
        fields = [
            'order_number', 'shipping_date',
            'sender_name', 'sender_address', 'sender_city', 'sender_email', 'sender_phone',
            'recipient_name', 'recipient_address', 'recipient_city', 'recipient_email', 'recipient_phone',
            'recipient_instructions',
            'weight', 'length', 'width', 'height',
            'carrier', 'carrier_other', 'tracking_number',
            'is_fragile', 'is_insured', 'insurance_amount',
            'cash_on_delivery', 'signature_required', 'recipient_message'
        ]
        widgets = {
            'order_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CMD-2025-0001'
            }),
            'shipping_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'value': date.today().isoformat()
            }),
            'sender_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom ou entreprise'
            }),
            'sender_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '123 Rue de la Paix'
            }),
            'sender_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '75001 Paris'
            }),
            'sender_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'contact@monentreprise.fr'
            }),
            'sender_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '01 23 45 67 89'
            }),
            'recipient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du destinataire'
            }),
            'recipient_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '456 Avenue du Client'
            }),
            'recipient_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '69001 Lyon'
            }),
            'recipient_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'client@exemple.fr'
            }),
            'recipient_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '06 12 34 56 78'
            }),
            'recipient_instructions': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Laisser chez le gardien, code 1234...'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '1.5'
            }),
            'length': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '30'
            }),
            'width': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '20'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '10'
            }),
            'carrier': forms.Select(attrs={
                'class': 'form-select'
            }),
            'carrier_other': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du transporteur'
            }),
            'tracking_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '3Y001234567890'
            }),
            'is_fragile': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'is_insured': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'insurance_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '150.00'
            }),
            'cash_on_delivery': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '100.00'
            }),
            'signature_required': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'recipient_message': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Merci pour votre commande !'
            }),
        }


class PackageItemForm(forms.ModelForm):
    """Formulaire pour un article du colis"""
    
    class Meta:
        model = TicketItem
        fields = ['description', 'quantity', 'value']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description de l\'article'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0.00'
            }),
        }


# Formset pour gérer plusieurs articles
PackageItemFormSet = formset_factory(
    PackageItemForm,
    extra=1,
    can_delete=True
)

