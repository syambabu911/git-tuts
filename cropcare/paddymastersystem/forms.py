
from django import forms
from .models import InterestEntry
from .models import PartyRecord, MillsRecord, AllRecords
from .models import LedgerEntry




class InterestEntryForm(forms.ModelForm):
    class Meta:
        model = InterestEntry
        fields = ['name', 'amount', 'transaction_type', 'interest_rate', 'date', 'is_paid']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class MillRecordForm(forms.ModelForm):
    class Meta:
        model = MillsRecord
        fields = '__all__'  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class PartyRecordForm(forms.ModelForm):
    class Meta:
        model = PartyRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            
        }



class AllRecordsForm(forms.ModelForm):
    class Meta:
        model = AllRecords
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class LedgerEntryForm(forms.ModelForm):
    class Meta:
        model = LedgerEntry
        fields = ['transaction_date', 'name', 'amount', 'party_or_mill', 'ac_name', 'payment_status']
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date','class':'ledgerentry'}),
             'name':forms.TextInput(attrs={'class':'ledgerentry'}),
             'amount':forms.TextInput(attrs={'class':'ledgerentry'}),
             'party_or_mill':forms.TextInput(attrs={'class':'ledgerentry'}),
             'ac_name':forms.TextInput(attrs={'class':'ledgerentry'}),
             'payment_status':forms.CheckboxInput(attrs={'class':'ledgerentry'}),
        }



