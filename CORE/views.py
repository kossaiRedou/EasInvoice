import json
import os
from pathlib import Path
from decimal import Decimal
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.forms import formset_factory
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.db import transaction

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print(f"WeasyPrint non disponible: {e}")

from .forms import InvoiceForm, ItemForm
from .models import Invoice, InvoiceItem, UserProfile, Client


def _build_items_from_formset(items_formset):
    items = []
    for form in items_formset:
        if not form.is_valid():
            continue
        cleaned = form.cleaned_data
        if not cleaned:
            continue
        if cleaned.get('DELETE'):
            continue
        desc = cleaned.get('description')
        qty = cleaned.get('quantity')
        price = cleaned.get('unit_price')
        if desc and qty is not None and price is not None:
            line_total = Decimal(str(qty)) * Decimal(str(price))
            items.append({
                'description': desc,
                'quantity': Decimal(str(qty)),
                'unit_price': Decimal(str(price)),
                'line_total': line_total,
            })
    return items


# ============== AUTHENTIFICATION ==============

def register_view(request):
    """Inscription d'un nouvel utilisateur"""
    if request.user.is_authenticated:
        return redirect('CORE:dashboard')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Créer le profil utilisateur
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Bienvenue {user.username} ! Votre compte a été créé.')
            return redirect('CORE:dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'CORE/register.html', {'form': form})


def login_view(request):
    """Connexion d'un utilisateur"""
    if request.user.is_authenticated:
        return redirect('CORE:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username} !')
                return redirect('CORE:dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'CORE/login.html', {'form': form})


def logout_view(request):
    """Déconnexion d'un utilisateur"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('CORE:login')


# ============== DASHBOARD ==============

@login_required
def dashboard(request):
    """Dashboard utilisateur avec statistiques et liste des factures"""
    invoices = Invoice.objects.filter(user=request.user).order_by('-created_at')
    
    # Statistiques
    total_invoices = invoices.count()
    paid_invoices = invoices.filter(status='paid').count()
    pending_invoices = invoices.filter(status__in=['draft', 'sent']).count()
    overdue_invoices = invoices.filter(status='overdue').count()
    
    # Montants
    total_revenue = sum([inv.total for inv in invoices.filter(status='paid')])
    pending_amount = sum([inv.total for inv in invoices.filter(status__in=['draft', 'sent', 'overdue'])])
    
    context = {
        'invoices': invoices[:10],  # Les 10 dernières
        'total_invoices': total_invoices,
        'paid_invoices': paid_invoices,
        'pending_invoices': pending_invoices,
        'overdue_invoices': overdue_invoices,
        'total_revenue': total_revenue,
        'pending_amount': pending_amount,
    }
    return render(request, 'CORE/dashboard.html', context)


# ============== GESTION DES FACTURES ==============

@login_required
def invoice_list(request):
    """Liste de toutes les factures de l'utilisateur"""
    invoices = Invoice.objects.filter(user=request.user)
    
    # Filtres
    status_filter = request.GET.get('status')
    if status_filter:
        invoices = invoices.filter(status=status_filter)
    
    return render(request, 'CORE/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_detail(request, invoice_id):
    """Détail d'une facture"""
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    return render(request, 'CORE/invoice_detail.html', {'invoice': invoice})


@login_required
def invoice_update_status(request, invoice_id):
    """Mettre à jour le statut d'une facture"""
    if request.method == 'POST':
        invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
        new_status = request.POST.get('status')
        if new_status in dict(Invoice.STATUS_CHOICES):
            invoice.status = new_status
            invoice.save()
            messages.success(request, f'Statut de la facture {invoice.invoice_number} mis à jour.')
    return redirect('CORE:invoice_detail', invoice_id=invoice_id)


@login_required
def invoice_delete(request, invoice_id):
    """Supprimer une facture"""
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    if request.method == 'POST':
        invoice_number = invoice.invoice_number
        invoice.delete()
        messages.success(request, f'Facture {invoice_number} supprimée.')
        return redirect('CORE:invoice_list')
    return render(request, 'CORE/invoice_confirm_delete.html', {'invoice': invoice})


@login_required
def invoice_download_pdf(request, invoice_id):
    """Télécharger le PDF d'une facture existante"""
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    
    # Préparer les items
    items = []
    for item in invoice.items.all():
        items.append({
            'description': item.description,
            'quantity': float(item.quantity),
            'unit_price': float(item.unit_price),
            'line_total': float(item.line_total),
        })
    
    # Préparer le contexte
    vat_note = "TVA non applicable, art. 293 B du CGI" if invoice.is_vat_exempt else None
    penalties_note = f"Pénalités de retard: {invoice.late_fee_rate}%/an à compter du lendemain de la date d'échéance." if invoice.late_fee_rate else None
    recovery_note = "Indemnité forfaitaire de recouvrement: 40 € due en cas de retard de paiement." if invoice.recovery_fee else None
    
    context = {
        'from_name': invoice.from_name,
        'from_address': invoice.from_address,
        'from_city': invoice.from_city,
        'from_email': invoice.from_email,
        'siret': invoice.siret,
        'rcs': invoice.rcs,
        'is_ei': invoice.is_ei,
        'to_name': invoice.to_name,
        'to_address': invoice.to_address,
        'to_city': invoice.to_city,
        'to_email': invoice.to_email,
        'invoice_number': invoice.invoice_number,
        'invoice_date': invoice.invoice_date,
        'service_date_start': invoice.service_date_start,
        'service_date_end': invoice.service_date_end,
        'due_date': invoice.due_date,
        'items': items,
        'is_vat_exempt': invoice.is_vat_exempt,
        'vat_rate': float(invoice.vat_rate),
        'subtotal': float(invoice.subtotal),
        'vat_amount': float(invoice.vat_amount),
        'total': float(invoice.total),
        'vat_note': vat_note,
        'payment_terms': invoice.payment_terms,
        'penalties_note': penalties_note,
        'recovery_note': recovery_note,
        'autoliquidation': invoice.autoliquidation,
    }
    
    html_string = render_to_string('CORE/invoice.html', context)
    
    if not WEASYPRINT_AVAILABLE:
        return HttpResponse("WeasyPrint n'est pas installé.", status=500)
    
    try:
        html = HTML(string=html_string, base_url=None)
        css_file = Path(__file__).resolve().parent.parent / 'static' / 'CORE' / 'css' / 'invoice.css'
        if css_file.exists():
            pdf = html.write_pdf(stylesheets=[CSS(css_file)])
        else:
            pdf = html.write_pdf()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"facture_{invoice.invoice_number}_{datetime.now().strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        import traceback
        return HttpResponse(f"Erreur: {str(e)}<br><pre>{traceback.format_exc()}</pre>", status=500)


# ============== CRÉATION DE FACTURE ==============

@login_required
def generate_invoice_form(request):
    """
    Affiche le formulaire de création de facture et sauvegarde dans la base de données.
    """
    ItemFormSet = formset_factory(ItemForm, extra=1, can_delete=True)
    
    # Récupérer le profil utilisateur pour pré-remplir
    try:
        profile = request.user.profile
        initial_data = {
            'from_name': profile.company_name or request.user.get_full_name() or request.user.username,
            'from_address': profile.address,
            'from_city': profile.city,
            'from_email': profile.email or request.user.email,
            'siret': profile.siret,
            'rcs': profile.rcs,
            'is_ei': profile.is_ei,
            'invoice_date': datetime.now().date(),
            'due_date': datetime.now().date(),
            'vat_rate': 20.00,
            'recovery_fee': True,
        }
    except UserProfile.DoesNotExist:
        # Créer le profil s'il n'existe pas
        profile = UserProfile.objects.create(user=request.user)
        initial_data = {
            'invoice_date': datetime.now().date(),
            'due_date': datetime.now().date(),
            'vat_rate': 20.00,
            'recovery_fee': True,
        }

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        items_formset = ItemFormSet(request.POST, prefix='items')
        
        if form.is_valid() and items_formset.is_valid():
            data = form.cleaned_data
            items = _build_items_from_formset(items_formset)
            
            # Fallback: si aucun item, utiliser les champs simples
            if not items and data.get('description'):
                qty = Decimal(str(data.get('quantity') or 1))
                price = Decimal(str(data.get('unit_price') or 0))
                items = [{
                    'description': data['description'],
                    'quantity': qty,
                    'unit_price': price,
                    'line_total': qty * price,
                }]
            
            # Totaux
            subtotal = Decimal('0')
            for it in items:
                subtotal += it['line_total']
            
            # Gestion TVA
            is_vat_exempt = bool(data.get('is_vat_exempt'))
            vat_rate_input = data.get('vat_rate') if data.get('vat_rate') is not None else Decimal('0')
            vat_rate = Decimal('0') if is_vat_exempt else Decimal(str(vat_rate_input))
            vat_amount = subtotal * (vat_rate / 100)
            total = subtotal + vat_amount
            
            # Sauvegarder la facture dans la base de données
            with transaction.atomic():
                invoice = Invoice.objects.create(
                    user=request.user,
                    from_name=data['from_name'],
                    from_address=data['from_address'],
                    from_city=data.get('from_city', ''),
                    from_email=data.get('from_email', ''),
                    siret=data.get('siret', ''),
                    rcs=data.get('rcs', ''),
                    is_ei=data.get('is_ei', False),
                    to_name=data['to_name'],
                    to_address=data['to_address'],
                    to_city=data.get('to_city', ''),
                    to_email=data.get('to_email', ''),
                    invoice_number=data['invoice_number'],
                    invoice_date=data['invoice_date'],
                    service_date_start=data.get('service_date_start'),
                    service_date_end=data.get('service_date_end'),
                    due_date=data['due_date'],
                    subtotal=subtotal,
                    vat_rate=vat_rate,
                    vat_amount=vat_amount,
                    total=total,
                    is_vat_exempt=is_vat_exempt,
                    payment_terms=data.get('payment_terms', ''),
                    late_fee_rate=data.get('late_fee_rate'),
                    recovery_fee=data.get('recovery_fee', False),
                    autoliquidation=data.get('autoliquidation', False),
                    status='draft',
                )
                
                # Sauvegarder les items
                for idx, item_data in enumerate(items):
                    InvoiceItem.objects.create(
                        invoice=invoice,
                        description=item_data['description'],
                        quantity=item_data['quantity'],
                        unit_price=item_data['unit_price'],
                        line_total=item_data['line_total'],
                        order=idx,
                    )
            
            messages.success(request, f'Facture {invoice.invoice_number} créée avec succès !')
            
            # Rediriger vers le téléchargement PDF
            return redirect('CORE:invoice_download_pdf', invoice_id=invoice.id)
    else:
        form = InvoiceForm(initial=initial_data)
        items_formset = ItemFormSet(prefix='items')
    
    return render(request, 'CORE/form.html', {
        'form': form,
        'items_formset': items_formset,
        'weasyprint_available': WEASYPRINT_AVAILABLE
    })


def add_item_row(request):
    """HTMX endpoint: retourne une ligne d'item vide et met à jour TOTAL_FORMS."""
    total_forms = request.POST.get('items-TOTAL_FORMS') or request.GET.get('items-TOTAL_FORMS')
    try:
        current_idx = int(total_forms)
    except (TypeError, ValueError):
        current_idx = 0
    new_index = current_idx
    ItemFormSet = formset_factory(ItemForm, extra=0, can_delete=True)
    dummy_formset = ItemFormSet(prefix='items')
    form = dummy_formset.empty_form
    form.prefix = f'items-{new_index}'
    row_html = render_to_string('CORE/_item_row.html', {'form': form, 'index': new_index})
    mgmt_html = f'\n<input type="hidden" name="items-TOTAL_FORMS" id="id_items-TOTAL_FORMS" value="{new_index + 1}" hx-swap-oob="true">\n'
    return HttpResponse(row_html + mgmt_html)


def privacy_policy(request):
    """Page de politique de confidentialité"""
    return render(request, 'CORE/privacy_policy.html')


# ============== GESTION DES CLIENTS ==============

@login_required
def client_list(request):
    """Liste des clients de l'utilisateur"""
    clients = Client.objects.filter(user=request.user)
    return render(request, 'CORE/client_list.html', {'clients': clients})


@login_required
def client_create(request):
    """Créer un nouveau client"""
    from .forms import ClientForm
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            messages.success(request, f'Client {client.name} créé avec succès !')
            return redirect('CORE:client_list')
    else:
        form = ClientForm()
    return render(request, 'CORE/client_form.html', {'form': form})


# ============== PAGE D'ACCUEIL PUBLIQUE ==============

def home(request):
    """Page d'accueil publique (ancienne vue generate_invoice_form sans auth)"""
    if request.user.is_authenticated:
        return redirect('CORE:dashboard')
    return render(request, 'CORE/home.html')
