from django.db import models
from django.utils import timezone


class Ticket(models.Model):
    """Étiquette d'expédition"""
    
    # Identification
    order_number = models.CharField(max_length=100, unique=True, verbose_name="Numéro de commande")
    created_at = models.DateTimeField(default=timezone.now)
    
    # Expéditeur
    sender_name = models.CharField(max_length=200, verbose_name="Nom/Entreprise expéditeur")
    sender_address = models.TextField(verbose_name="Adresse expéditeur")
    sender_city = models.CharField(max_length=100, verbose_name="Ville expéditeur")
    sender_email = models.EmailField(blank=True, verbose_name="Email expéditeur")
    sender_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone expéditeur")
    
    # Destinataire
    recipient_name = models.CharField(max_length=200, verbose_name="Nom destinataire")
    recipient_address = models.TextField(verbose_name="Adresse destinataire")
    recipient_city = models.CharField(max_length=100, verbose_name="Ville destinataire")
    recipient_email = models.EmailField(blank=True, verbose_name="Email destinataire")
    recipient_phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone destinataire")
    recipient_instructions = models.CharField(max_length=200, blank=True, verbose_name="Instructions de livraison")
    
    # Colis
    shipping_date = models.DateField(verbose_name="Date d'expédition")
    weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Poids (kg)")
    length = models.IntegerField(verbose_name="Longueur (cm)")
    width = models.IntegerField(verbose_name="Largeur (cm)")
    height = models.IntegerField(verbose_name="Hauteur (cm)")
    
    CARRIER_CHOICES = [
        ('colissimo', 'Colissimo'),
        ('chronopost', 'Chronopost'),
        ('mondial_relay', 'Mondial Relay'),
        ('ups', 'UPS'),
        ('dpd', 'DPD'),
        ('other', 'Autre'),
    ]
    carrier = models.CharField(max_length=50, choices=CARRIER_CHOICES, verbose_name="Transporteur")
    carrier_other = models.CharField(max_length=100, blank=True, verbose_name="Autre transporteur")
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name="Numéro de suivi")
    
    # Options
    is_fragile = models.BooleanField(default=False, verbose_name="Fragile")
    is_insured = models.BooleanField(default=False, verbose_name="Assuré")
    insurance_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Montant assuré")
    cash_on_delivery = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Contre-remboursement")
    signature_required = models.BooleanField(default=False, verbose_name="Signature obligatoire")
    recipient_message = models.CharField(max_length=100, blank=True, verbose_name="Message au destinataire")
    
    # Métadonnées
    pdf_generated = models.BooleanField(default=False)
    invoice_generated = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Étiquette"
        verbose_name_plural = "Étiquettes"
    
    def __str__(self):
        return f"Étiquette {self.order_number}"
    
    def get_carrier_display_name(self):
        """Retourne le nom du transporteur pour affichage"""
        if self.carrier == 'other' and self.carrier_other:
            return self.carrier_other
        return self.get_carrier_display()
    
    def get_total_value(self):
        """Calcule la valeur totale du colis"""
        return sum(item.get_line_total() for item in self.items.all())


class TicketItem(models.Model):
    """Article dans un colis"""
    ticket = models.ForeignKey(Ticket, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=500, verbose_name="Description")
    quantity = models.IntegerField(default=1, verbose_name="Quantité")
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valeur unitaire")
    
    def get_line_total(self):
        return self.quantity * self.value
    
    def __str__(self):
        return f"{self.quantity}x {self.description}"
    
    class Meta:
        verbose_name = "Article du colis"
        verbose_name_plural = "Articles du colis"
