from django.db import models
from django.utils import timezone


class BusinessProfile(models.Model):
    name    = models.CharField(max_length=200)
    email   = models.EmailField()
    address = models.TextField()
    phone   = models.CharField(max_length=20)
    logo    = models.ImageField(upload_to='logos/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Business Profile"


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent',  'Sent'),
        ('paid',  'Paid'),
    ]

    client_name    = models.CharField(max_length=200, default='')
    client_email   = models.EmailField(default='')
    client_phone   = models.CharField(max_length=20, default='')
    client_address = models.TextField(default='')

    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    issue_date     = models.DateField(auto_now_add=True)
    due_date       = models.DateField()
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    notes          = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            year  = timezone.now().year
            month = timezone.now().month
            last  = Invoice.objects.filter(
                invoice_number__startswith=f'INV-{year}{month:02d}-'
            ).order_by('invoice_number').last()

            new_num = (int(last.invoice_number.split('-')[-1]) + 1) if last else 1
            self.invoice_number = f'INV-{year}{month:02d}-{new_num:04d}'

        super().save(*args, **kwargs)

    @property
    def total_amount(self):
        return sum(item.total for item in self.items.all())



    def __str__(self):
        return f"Invoice #{self.invoice_number} — {self.client_name}"


class InvoiceItem(models.Model):
    invoice     = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=300)
    quantity    = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price  = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return self.description