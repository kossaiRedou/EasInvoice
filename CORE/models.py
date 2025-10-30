from django.db import models
from django.utils import timezone


class Invoice(models.Model):
    """Facture"""
    
    # Lien avec étiquette (optionnel)
    ticket = models.OneToOneField(
        'TICKET.Ticket',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='invoice'
    )
    
    # Identification
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Émetteur
    from_name = models.CharField(max_length=200)
    from_address = models.TextField()
    from_city = models.CharField(max_length=100)
    from_email = models.EmailField(blank=True)
    siret = models.CharField(max_length=14, blank=True)
    rcs = models.CharField(max_length=100, blank=True)
    is_ei = models.BooleanField(default=False)
    
    # Destinataire
    to_name = models.CharField(max_length=200)
    to_address = models.TextField()
    to_city = models.CharField(max_length=100)
    to_email = models.EmailField(blank=True)
    
    # Dates
    service_date_start = models.DateField(null=True, blank=True)
    service_date_end = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    
    # Montants
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    is_vat_exempt = models.BooleanField(default=False)
    
    # Conditions
    payment_terms = models.TextField(blank=True)
    late_fee_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    recovery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=40)
    autoliquidation = models.BooleanField(default=False)
    
    # Métadonnées
    pdf_generated = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Facture {self.invoice_number}"


class InvoiceItem(models.Model):
    """Ligne de facture"""
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def get_line_total(self):
        return self.quantity * self.unit_price
    
    def __str__(self):
        return f"{self.quantity}x {self.description}"
