from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from .models import Invoice, BusinessProfile
from .forms import InvoiceForm, InvoiceItemFormSet
from .utils import amount_to_words      


def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoices/list.html', {'invoices': invoices})


def invoice_create(request):
    if request.method == 'POST':
        form    = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice         = form.save()       # client fields saved directly
            formset.instance = invoice
            formset.save()
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form    = InvoiceForm()
        formset = InvoiceItemFormSet()

    return render(request, 'invoices/form.html', {'form': form, 'formset': formset})


def invoice_detail(request, pk):
    invoice  = get_object_or_404(Invoice, pk=pk)
    business = BusinessProfile.objects.first()
    return render(request, 'invoices/detail.html', {
        'invoice':  invoice,
        'business': business,
        'amount_in_words': amount_to_words(invoice.total_amount)
    })


from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Invoice, BusinessProfile
from weasyprint import HTML
from django.conf import settings


def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    business = BusinessProfile.objects.first()

    html = render_to_string('invoices/pdf_template.html', {
        'invoice': invoice,
        'business': business,
        'MEDIA_URL': settings.MEDIA_URL,
    })

    pdf = HTML(
        string=html,
        base_url=request.build_absolute_uri('/')   # 🔥 IMPORTANT FIX
    ).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice_{invoice.invoice_number}.pdf"'

    return response