# Example models.py
from django.db import models
from django.contrib.auth.models import User


class RecordDetails(models.Model):
    party_name = models.CharField(max_length=100)
    party_address = models.CharField(max_length=255)
    mill_name = models.CharField(max_length=100)
    mill_place = models.CharField(max_length=100)
 


from django.db import models
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
 
class InterestEntry(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    is_paid = models.BooleanField(default=False)
    earned_interest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calculate interest
        today = timezone.now().date()
        days_difference = Decimal((today - self.date).days)
        if days_difference > 0:
            interest = (self.amount * self.interest_rate / Decimal(100)) * (days_difference / Decimal(365))
        else:
            interest = Decimal(0)
        self.earned_interest = interest
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.transaction_type} - {self.amount}"






class AllRecords(models.Model):
    date = models.DateField()
    kl_no = models.CharField(max_length=100)
    mill_name = models.CharField(max_length=100)
    mill_place = models.CharField(max_length=100)
    mill_rate = models.FloatField()
    mill_weight = models.FloatField()
    mill_remarks = models.TextField(blank=True, null=True)
    mill_total_wages = models.FloatField()
    party_name = models.CharField(max_length=100)
    party_address = models.CharField(max_length=200)
    party_weight = models.FloatField()
    paddy_variety = models.CharField(max_length=100)
    lorry_no = models.CharField(max_length=100)
    lorry_advance = models.FloatField()
    lorry_total_fare = models.FloatField()
    gennius_qty = models.FloatField()
    gennius_price = models.FloatField()
    MILL_CALCULATION_CHOICES = [
        ('BAGS_X4', 'BAGS X 4'), 
        ('78KGS', '78 KGS'), 
        ('79KGS', '79 KGS'), 
        ('79_Delivery', '79 Delivery'), 
        ('78_Delivery', '78 Delivery'), 
        ('BAGS_X4_Delivery', 'BAGS X 4 Delivery'),
    ]

    mill_calculation_type = models.CharField(choices=MILL_CALCULATION_CHOICES, max_length=50)
    mill_rate_type = models.CharField(max_length=100, choices=(('party rate', 'party rate'), ('mill rate', 'mill rate')))
    PARTY_CALCULATION_CHOICES = [
        ('BAGS_X4', 'BAGS X 4'), 
        ('78KGS', '78 KGS'), 
        ('79KGS', '79 KGS'), 
        ('79_Delivery', '79 Delivery'), 
        ('78_Delivery', '78 Delivery'), 
        ('BAGS_X4_Delivery', 'BAGS X 4 Delivery'),
    ]
    party_calculation_type = models.CharField(choices=PARTY_CALCULATION_CHOICES, max_length=50)
    party_rate_type = models.CharField(max_length=100, choices=(('mill rate', 'mill rate'), ('party rate', 'party rate')))

class MillsRecord(models.Model):
    date = models.DateField()
    kl_no = models.CharField(max_length=100)
    mill_name = models.CharField(max_length=100)
    mill_place = models.CharField(max_length=100)
    mill_rate = models.DecimalField(max_digits=10, decimal_places=2)
    mill_weight = models.DecimalField(max_digits=10, decimal_places=2)
    mill_remarks = models.TextField(blank=True)
    mill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    MILL_CALCULATION_CHOICES = [
        ('BAGS_X4', 'BAGS X 4'),
        ('78KGS', '78 KGS'),
        ('79KGS', '79 KGS'),
        ('79_Delivery', '79 Delivery'),
        ('78_Delivery', '78 Delivery'),
        ('BAGS_X4_Delivery', 'BAGS X 4 Delivery'),
    ]
    mill_calculation_type = models.CharField(choices=MILL_CALCULATION_CHOICES, max_length=50)
    mill_rate_type = models.CharField(max_length=100, choices=(('party rate', 'party rate'), ('mill rate', 'mill rate')))
    payment_status = models.BooleanField(default=False)

class PartyRecord(models.Model):
    date = models.DateField()
    kl_no = models.CharField(max_length=100)
    party_name = models.CharField(max_length=100)
    party_address = models.CharField(max_length=200)
    party_weight = models.DecimalField(max_digits=10, decimal_places=2)
    party_rate = models.DecimalField(max_digits=10, decimal_places=2)
    paddy_variety = models.CharField(max_length=100)
    lorry_no = models.CharField(max_length=50)
    lorry_advance = models.DecimalField(max_digits=10, decimal_places=2)
    lorry_total_fare = models.DecimalField(max_digits=10, decimal_places=2)
    gennius_qty = models.IntegerField()
    party_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gennius_price = models.DecimalField(max_digits=10, decimal_places=2)
    PARTY_CALCULATION_CHOICES = [
        ('BAGS_X4', 'BAGS X 4'),
        ('78KGS', '78 KGS'),
        ('79KGS', '79 KGS'),
        ('79_Delivery', '79 Delivery'),
        ('78_Delivery', '78 Delivery'),
        ('BAGS_X4_Delivery', 'BAGS X 4 Delivery'),
    ]
    party_calculation_type = models.CharField(choices=PARTY_CALCULATION_CHOICES, max_length=50)
    party_rate_type = models.CharField(max_length=100, choices=(('mill rate', 'mill rate'), ('party rate', 'party rate')))
    payment_status = models.BooleanField(default=False)

class LedgerEntry(models.Model):
    transaction_date= models.DateField()
    name= models.CharField(max_length=100)
    amount= models.DecimalField(max_digits=10, decimal_places=2)
    party_or_mill= models.CharField(max_length=50)
    ac_name= models.CharField(max_length=100)
    created_at= models.DateTimeField(auto_now_add=True)
    payment_status= models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.transaction_date}"







