from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal, ROUND_HALF_UP


class UserProfile(models.Model):
    """Profil utilisateur étendu avec informations de facturation"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    company_name = models.CharField(max_length=200, verbose_name="Nom de l'entreprise", blank=True)
    address = models.TextField(verbose_name="Adresse", blank=True)
    city = models.CharField(max_length=100, verbose_name="Ville", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    siret = models.CharField(max_length=20, verbose_name="SIRET", blank=True)
    rcs = models.CharField(max_length=100, verbose_name="RCS", blank=True)
    is_ei = models.BooleanField(default=False, verbose_name="Entrepreneur Individuel")
    phone = models.CharField(max_length=20, verbose_name="Téléphone", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"


class Client(models.Model):
    """Clients récurrents d'un utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=200, verbose_name="Nom/Entreprise")
    address = models.TextField(verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Téléphone", blank=True)
    notes = models.TextField(verbose_name="Notes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ['-created_at']


class Invoice(models.Model):
    """Facture"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('sent', 'Envoyée'),
        ('paid', 'Payée'),
        ('overdue', 'En retard'),
        ('cancelled', 'Annulée'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    
    # Informations émetteur (copie du profil au moment de la création)
    from_name = models.CharField(max_length=200, verbose_name="Nom/Entreprise émetteur")
    from_address = models.TextField(verbose_name="Adresse émetteur")
    from_city = models.CharField(max_length=100, verbose_name="Ville émetteur", blank=True)
    from_email = models.EmailField(verbose_name="Email émetteur", blank=True)
    siret = models.CharField(max_length=20, verbose_name="SIRET", blank=True)
    rcs = models.CharField(max_length=100, verbose_name="RCS", blank=True)
    is_ei = models.BooleanField(default=False, verbose_name="Entrepreneur Individuel")
    
    # Informations destinataire
    to_name = models.CharField(max_length=200, verbose_name="Nom/Entreprise client")
    to_address = models.TextField(verbose_name="Adresse client")
    to_city = models.CharField(max_length=100, verbose_name="Ville client", blank=True)
    to_email = models.EmailField(verbose_name="Email client", blank=True)
    
    # Informations facture
    invoice_number = models.CharField(max_length=50, verbose_name="Numéro de facture")
    invoice_date = models.DateField(verbose_name="Date d'émission", default=timezone.now)
    service_date_start = models.DateField(verbose_name="Début de prestation", null=True, blank=True)
    service_date_end = models.DateField(verbose_name="Fin de prestation", null=True, blank=True)
    due_date = models.DateField(verbose_name="Date d'échéance")
    
    # Montants
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total HT", default=0)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Taux TVA (%)", default=20)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant TVA", default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total TTC", default=0)
    is_vat_exempt = models.BooleanField(default=False, verbose_name="Franchise de TVA")
    
    # Conditions de paiement
    payment_terms = models.TextField(verbose_name="Modalités de paiement", blank=True)
    late_fee_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Pénalités de retard (%)", null=True, blank=True)
    recovery_fee = models.BooleanField(default=True, verbose_name="Indemnité de recouvrement (40€)")
    autoliquidation = models.BooleanField(default=False, verbose_name="Autoliquidation")
    
    # État et suivi
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="État")
    notes = models.TextField(verbose_name="Notes internes", blank=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Facture {self.invoice_number} - {self.to_name}"

    def calculate_totals(self):
        """Recalcule les totaux à partir des items"""
        items = self.items.all()
        self.subtotal = sum([item.line_total for item in items])
        if self.is_vat_exempt:
            self.vat_amount = Decimal('0.00')
        else:
            self.vat_amount = self.subtotal * (self.vat_rate / 100).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.total = (self.subtotal + self.vat_amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.save()

    def is_overdue(self):
        """Vérifie si la facture est en retard"""
        if self.status != 'paid' and self.due_date < timezone.now().date():
            return True
        return False

    def get_status_badge_class(self):
        """Retourne la classe CSS Bootstrap pour le badge de statut"""
        status_classes = {
            'draft': 'bg-secondary',
            'sent': 'bg-info',
            'paid': 'bg-success',
            'overdue': 'bg-danger',
            'cancelled': 'bg-dark',
        }
        return status_classes.get(self.status, 'bg-secondary')

    class Meta:
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        ordering = ['-invoice_date', '-created_at']
        unique_together = [['user', 'invoice_number']]


class InvoiceItem(models.Model):
    """Ligne d'article d'une facture"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=500, verbose_name="Description")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantité", default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire HT")
    line_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total ligne", default=0)
    order = models.IntegerField(default=0, verbose_name="Ordre")

    def save(self, *args, **kwargs):
        """Calcule automatiquement le total de ligne"""
        self.line_total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description} - {self.line_total}€"

    class Meta:
        verbose_name = "Ligne de facture"
        verbose_name_plural = "Lignes de facture"
        ordering = ['order', 'id']


class ContactMessage(models.Model):
    """Messages envoyés depuis la page d'accueil (contact)"""
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom", blank=True)
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=30, verbose_name="Téléphone", blank=True)
    message = models.TextField(verbose_name="Message")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']
