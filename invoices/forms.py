from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Invoice, InvoiceItem


# =========================
# Invoice Form
# =========================
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'client_name', 'client_email', 'client_phone', 'client_address',
            'due_date', 'status', 'notes',
        ]
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Client name'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'client_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number'
            }),
            'client_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Address'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notes...'
            }),
        }

    def clean_client_phone(self):
        phone = self.cleaned_data.get('client_phone')
        if phone and len(phone) < 10:
            raise forms.ValidationError("Phone number is too short.")
        return phone


# =========================
# Invoice Item Form
# =========================
class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['description', 'quantity', 'unit_price']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item description'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
        }


# =========================
# Custom Formset Validation
# =========================
class BaseItemFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_item = False

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                has_item = True

        if not has_item:
            raise ValidationError("At least one item is required.")


# =========================
# Formset
# =========================
InvoiceItemFormSet = inlineformset_factory(
    Invoice,
    InvoiceItem,
    form=InvoiceItemForm,
    formset=BaseItemFormSet,
    extra=1,
    can_delete=True
)