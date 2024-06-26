from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import InterestEntry,MillsRecord,PartyRecord, LedgerEntry
from .forms import MillRecordForm, PartyRecordForm,AllRecords,AllRecordsForm, LedgerEntryForm, InterestEntryForm
from datetime import datetime  
import requests 
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def register(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST['user_type']
        user = User.objects.create_user(username=username, email=email, password=password)
        if user_type == 'active':
            user.is_active = True
        elif user_type == 'staff':
            user.is_staff = True
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login(request, user)
            return redirect('login')
    return render(request, 'credential/register.html')


def adminregister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_superuser=True
        user.is_staff = True
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            return redirect('login')
    return render(request, 'credential/adminregister.html')
    

def login_view(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'credential/login.html')




'''from django.core.mail import send_mail
from django.conf import settings
import random
import string

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {'error_message': 'Please enter both username and password'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                otp = generate_otp()
                request.session['otp'] = otp
                request.session['user_id'] = user.id

                # Send OTP via email to superuser
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return redirect('enter_otp')
            elif user.is_active and user.is_staff:
                recipient_email = 'syambabu911@gmail.com'

                # Send login notification to the staff user
                send_mail(
                    'Login Notification',
                    'You have successfully logged in.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )

                # Send login notification to the specified recipient
                send_mail(
                    'Staff Login Notification',
                    f'The staff user {user.username} has successfully logged in.',
                    settings.EMAIL_HOST_USER,
                    [recipient_email],
                    fail_silently=False,
                )

                login(request, user)
                return redirect('homepage')
            else:
                login(request, user)
                return redirect('homepage')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'credential/login.html')'''




def enter_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('otp')
        user_id = request.session.get('user_id')

        if entered_otp == stored_otp:
            user = User.objects.get(id=user_id)
            login(request, user)
            request.session.pop('otp', None)
            request.session.pop('user_id', None)
            return redirect('homepage')
        else:
            return render(request, 'credential/enter_otp.html', {'error_message': 'Invalid OTP'})

    return render(request, 'credential/enter_otp.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
def common(request):
    return render(request,'common.html')

import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
logger = logging.getLogger(__name__)
@login_required(login_url='login')
def homepage(request):
    url = 'https://www.timeanddate.com/'
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status() 
        soup = BeautifulSoup(res.content, 'html.parser')
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        default_city ='Hyderabad'
        temp_element = soup.find('span', class_='cur-temp')
        condition = temp_element['title'] if temp_element else "N/A"   
        temp = temp_element.text if temp_element else "N/A"
        return render(request, 'homepage/homepage.html', {
            'city': default_city, 
            'temp': temp, 
            'condition': condition, 
            'date': now,
            'current_time': current_time
        })
    except requests.exceptions.Timeout:
        logger.error("Request to timeanddate.com timed out")
        return HttpResponse("The request timed out. Please try again later.", status=504)
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return HttpResponse("An error occurred while fetching data.", status=500)

@login_required(login_url='login')
def add_party_record(request):
    if request.method == 'POST':
        form = PartyRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'party/add_party_record.html', {'msg':'record create sucessfully','form':  PartyRecordForm()})
            #return redirect('party')
    else:
        form = PartyRecordForm()
    return render(request, 'party/add_party_record.html', {'form': form})

@login_required(login_url='login')
def add_mill_record(request):
    if request.method == 'POST':
        form = MillRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'mills/add_mill_record.html', {'msg':'record create sucessfully','form':MillRecordForm()})
            #return redirect('mills')
        else:
            return render(request, 'mills/add_mill_record.html', {'form':form})  
    else:
        form = MillRecordForm()
    return render(request, 'mills/add_mill_record.html', {'form': form})

@login_required(login_url='login')
def mills(request):
    mill_records = MillsRecord.objects.all()
    paginator = Paginator(mill_records, 10)  # Show 10 mills per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'mills/mills.html', context)


@login_required(login_url='login')
def mills_detail_view(request, pk):
    mill_record = get_object_or_404(MillsRecord, pk=pk)
    ledger_entries = LedgerEntry.objects.all()
    total_amount = ledger_entries.aggregate(Sum('amount'))['amount__sum'] or 0
    amount_paid = ledger_entries.filter(payment_status=True).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_amount - amount_paid
    context = {
        'mill_record': mill_record,
        'total_amount': total_amount,
        'amount_paid': amount_paid,
        'balance': balance,
    }

    return render(request, 'mills/mill_record_form.html', context)

@login_required(login_url='login')
def edit_mills_record(request, pk):
    mills_record = get_object_or_404(MillsRecord, pk=pk)
    if request.method == 'POST':
        form = MillRecordForm(request.POST, instance=mills_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mills record updated successfully.')
            return redirect('mills_detail_view', pk=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MillRecordForm(instance=mills_record)

    return render(request, 'mills/edit_mills_record.html', {'form': form})

@login_required(login_url='login')
def party(request):
    party_records = PartyRecord.objects.all()
    paginator = Paginator(party_records, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'party/party.html', {'page_obj': page_obj})

@login_required(login_url='login')
def party_detail_view(request, pk):
    party_record = get_object_or_404(PartyRecord, pk=pk)
    ledger_entries = LedgerEntry.objects.all()
    total_amount = ledger_entries.aggregate(Sum('amount'))['amount__sum'] or 0
    amount_paid = ledger_entries.filter(payment_status=True).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_amount - amount_paid
    context = {
        'party_record': party_record,
        'total_amount': total_amount,
        'amount_paid': amount_paid,
        'balance': balance,
    }

    return render(request, 'party/party_record_form.html', context)

@login_required(login_url='login')
def edit_party_record(request, pk):
    party_record = get_object_or_404(PartyRecord, pk=pk)
    if request.method == 'POST':
        form = PartyRecordForm(request.POST, instance=party_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Party record updated successfully.')
            return redirect('party_detail_view', pk=pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PartyRecordForm(instance=party_record)

    return render(request, 'party/edit_party_record.html', {'form': form})

@login_required(login_url='login')
def create_record(request):
    if request.method == 'POST':
        form = AllRecordsForm(request.POST)
        if form.is_valid():
            record = form.save()
            return render(request, 'homepage/create_record.html', {'msg':'record create sucessfully','form': AllRecordsForm()})
            #return redirect('record_details')
    else:
        form = AllRecordsForm()
    return render(request, 'homepage/create_record.html', {'form': form})

@login_required(login_url='login')
def record_details(request):
    records = AllRecords.objects.all()  
    return render(request, 'homepage/record_details.html', {'records': records})

@login_required(login_url='login')
def interest_entry(request):
    if request.method == 'POST':
        form = InterestEntryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data successfully submitted.')
            return redirect('interest_entry')
        else:
            messages.error(request, 'Failed to submit data. Please check the form.')
    else:
        form = InterestEntryForm()
    return render(request, 'itc/interest_entry.html', {'form': form})


@login_required(login_url='login')
def view_credits(request):
    credits = InterestEntry.objects.filter(transaction_type='credit')
    return render(request, 'itc/viewcredits.html', {'entries': credits})

def delete_credit(request, entry_id):
    entry = get_object_or_404(InterestEntry, id=entry_id)
    entry.delete()
    return redirect('view_credits')

@login_required(login_url='login')
def view_debits(request):
    debits = InterestEntry.objects.filter(transaction_type='debit')
    return render(request, 'itc/viewdebits.html', {'entries': debits})

def delete_debit(request, entry_id):
    entry = get_object_or_404(InterestEntry, id=entry_id)
    entry.delete()
    return redirect('view_debits')

@login_required(login_url='login')
def success(request):
    return render(request, 'messages&errors/success.html')

@login_required(login_url='login')
def ledger(request):
    ledger_entries = LedgerEntry.objects.all()
    party_records = PartyRecord.objects.all()
    mills_records = MillsRecord.objects.all()
    total_amount = sum(ledger.amount for ledger in ledger_entries)
    total_mill_amount = sum(mills_record.mill_amount for mills_record in mills_records)
    total_party_amount = sum(party_record.party_rate * party_record.party_weight for party_record in party_records)
    mill_paid = sum(ledger.amount for ledger in ledger_entries if ledger.party_or_mill == 'mill' and ledger.payment_status)
    party_paid = sum(ledger.amount for ledger in ledger_entries if ledger.party_or_mill == 'party' and ledger.payment_status)
    mill_balance = total_mill_amount - mill_paid
    party_balance = total_party_amount - party_paid

    context = {
        'ledger_entries': ledger_entries,
        'party_records': party_records,
        'mills_records': mills_records,
        'total_amount': total_amount,
        'total_mill_amount': total_mill_amount,
        'total_party_amount': total_party_amount,
        'mill_paid': mill_paid,
        'party_paid': party_paid,
        'mill_balance': mill_balance,
        'party_balance': party_balance,
    }
    return render(request, 'ledger/ledger.html', context)


from django.http import HttpResponse
import csv
@login_required(login_url='login')
def download_pl_report(request):
    party_records = PartyRecord.objects.all()
    mills_records = MillsRecord.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pl_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['SL.NO', 'KL.NO', 'Mill Name', 'Party Name', 'Mill Amount', 'Party Amount', 'Profit/Loss'])
    for index, (party_record, mills_record) in enumerate(zip(party_records, mills_records), start=1):
        mill_amount = mills_record.mill_amount
        party_amount = party_record.party_amount
        profit_loss = party_amount - mill_amount 
        writer.writerow([index, party_record.kl_no, mills_record.mill_name, party_record.party_name, mill_amount, party_amount, profit_loss])
    return response

from django.db.models import Q
@login_required(login_url='login')
def search_records_mills(request):
    query = request.GET.get('search_query', '')
    mills_records = MillsRecord.objects.filter(
        Q(mill_name__icontains=query) |
        Q(kl_no__icontains=query)
    )
    context = {
        'query': query,
        'mills_records': mills_records,
    }
    return render(request, 'mills/search_results.html', context)

@login_required(login_url='login')
def search_records_party(request):
    query = request.GET.get('search_query', '')
    party_records = PartyRecord.objects.filter(
        Q(party_name__icontains=query) |
        Q(lorry_no__icontains=query)
    )
    context = {
        'query': query,
        'party_records': party_records,
    }
    return render(request, 'party/search_results1.html', context)

@login_required(login_url='login')
def search_records_pnl(request):
    query = request.GET.get('search_query', '')
    party_results = PartyRecord.objects.filter(party_name__icontains=query)
    mill_results = MillsRecord.objects.filter(mill_name__icontains=query)
    total_mill_amount = sum(record.mill_amount for record in mill_results)
    total_party_amount = sum(record.party_amount for record in party_results)
    transactions = []
    for party, mill in zip(party_results, mill_results):
        transactions.append({
            'kl_no': party.kl_no if party else mill.kl_no,
            'mill_name': mill.mill_name if mill else '',
            'party_name': party.party_name if party else '',
            'mill_amount': mill.mill_amount if mill else 0,
            'party_amount': party.party_amount if party else 0,
            'net_profit_loss': party.party_amount - mill.mill_amount if party and mill else 0  # Adjust according to your calculation
        })
    for party in party_results[len(mill_results):]:
        transactions.append({
            'kl_no': party.kl_no,
            'mill_name': 'Not avaialable',
            'party_name': party.party_name,
            'mill_amount': 0,
            'party_amount': party.party_amount,
            'net_profit_loss': party.party_amount
        })
    for mill in mill_results[len(party_results):]:
        transactions.append({
            'kl_no': mill.kl_no,
            'mill_name': mill.mill_name,
            'party_name': 'Not available',
            'mill_amount': mill.mill_amount,
            'party_amount': 0,
            'net_profit_loss': mill.mill_amount 
        })
    context = {
        'query': query,
        'transactions': transactions,
        'total_mill_amount': total_mill_amount,
        'total_party_amount': total_party_amount,
        'net_profit_loss': total_party_amount - total_mill_amount, 
    }
    return render(request, 'pnl/search_results2.html', context)




@login_required(login_url='login')
def search_records_ledger(request):
    query = request.GET.get('search_query', '')
    ledger_entries = LedgerEntry.objects.filter(
        Q(name__icontains=query) |
        Q(ac_name__icontains=query)
    )
    
    context = {
        'query': query,
        'ledger_entries': ledger_entries,
    }
    
    return render(request, 'view_ledger/search_results_ledger.html', context)



from django.db.models import Sum
@login_required(login_url='login')
def view_ledger(request):
    ledger_entries = LedgerEntry.objects.all()
    total_amount = ledger_entries.aggregate(Sum('amount'))['amount__sum'] or 0
    amount_paid = ledger_entries.filter(payment_status=True).aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_amount - amount_paid

    context = {
        'ledger_entries': ledger_entries,
        'total_amount': total_amount,
        'amount_paid': amount_paid,
        'balance': balance,
    }

    return render(request, 'view_ledger/view_ledger.html', context)

@user_passes_test(lambda user: user.is_superuser, login_url='calculator')
def add_ledger_entry(request):
    if request.method == "POST":
        form = LedgerEntryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'data inserted sucesssfully')
            messages.success(request,' You also add entry...!')
            return render(request, 'add_ledger_entry.html', {'form': LedgerEntryForm()})
        else:
            messages.error(request,' Data not inserted')
            messages.error(request,' Please try again')
    else:
        form = LedgerEntryForm()
    return render(request, 'ledger/add_ledger_entry.html', {'form': form})


@user_passes_test(lambda user: user.is_superuser, login_url='view_ledger')
def delete_ledger_entry(request, entry_id):
    ledger_entry = get_object_or_404(LedgerEntry, id=entry_id)
    if request.method == "POST":
        ledger_entry.delete()
        return redirect('view_ledger')
    return render(request, 'view_ledger/delete_ledger_entry.html', {'ledger_entry': ledger_entry})


@login_required(login_url='login')
def edit_ledger_entry(request, pk):
    ledger_entry = LedgerEntry.objects.get(pk=pk)
    if request.method == "POST":
        form = LedgerEntryForm(request.POST, instance=ledger_entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data updated sucessfully.')
            return redirect('view_ledger')
    else:
        form = LedgerEntryForm(instance=ledger_entry)
    return render(request, 'view_ledger/edit_ledger.html', {'form': form})


@login_required(login_url='login')
def view_records(request):
    party_records = PartyRecord.objects.all()
    mills_records = MillsRecord.objects.all()
    transactions = []
    total_mill_amount = 0
    total_party_amount = 0
    for party_record, mills_record in zip(party_records, mills_records):
        if mills_record:
            mill_amount = mills_record.mill_rate * mills_record.mill_weight
            party_amount = party_record.party_rate * party_record.party_weight
            total_mill_amount += mill_amount
            total_party_amount += party_amount
            net_profit_loss = mill_amount - party_amount
            transactions.append({
                'kl_no': mills_record.kl_no,
                'mill_name': mills_record.mill_name,
                'party_name': party_record.party_name,
                'mill_amount': mill_amount,
                'party_amount': party_amount,
                'net_profit_loss': net_profit_loss,
            })
        else:
            party_amount = party_record.party_rate * party_record.party_weight
            transactions.append({
                'kl_no': 'N/A', 
                'mill_name': 'N/A',  
                'party_name': party_record.party_name,
                'mill_amount': 0,
                'party_amount': party_amount,
                'net_profit_loss': -party_amount, 
            })

    context = {
        'transactions': transactions,
        'total_mill_amount': total_mill_amount,
        'total_party_amount': total_party_amount,
        'neft_profit_loss': total_mill_amount - total_party_amount,
    }
    return render(request, 'pnl/view_records.html', context)
import csv
@login_required(login_url='login')
def download_ledger_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ledger_entries.csv"'

    writer = csv.writer(response)
    writer.writerow(['SL.NO', 'Transaction Date', 'Name', 'Amount', 'Party/Mills', 'Account Name', 'Created At', 'Status'])

    ledger_entries = LedgerEntry.objects.all()

    for index, entry in enumerate(ledger_entries, start=1):
        writer.writerow([
            index,
            entry.transaction_date,
            entry.name,
            entry.amount,
            entry.party_or_mill,
            entry.ac_name,
            entry.created_at.strftime("%b %d, %Y, %I:%M %p"),
            'Paid' if entry.payment_status else 'Unpaid'
        ])

    return response

import csv
@login_required(login_url='login')
def download_party_record_details(request, pk):
    party_record = PartyRecord.objects.get(pk=pk)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="party_record_{party_record.pk}.txt"'
    writer = csv.writer(response)
    writer.writerow(['Party Name', 'Date', 'Party Address', 'Party Weight', 'Party Rate', 'Paddy Variety', 'Lorry No', 'Lorry Advance', 'Total Fare', 'Gennius Qty', 'Gennius Price', 'Rate Type', 'Calculation Type', 'Party Amount', 'Status'])
    writer.writerow([
        party_record.party_name,
        party_record.date,
        party_record.party_address,
        party_record.party_weight,
        party_record.party_rate,
        party_record.paddy_variety,
        party_record.lorry_no,
        party_record.lorry_advance,
        party_record.lorry_total_fare,
        party_record.gennius_qty,
        party_record.gennius_price,
        party_record.party_rate_type,
        party_record.party_calculation_type,
        party_record.party_amount,
        'Paid' if party_record.payment_status else 'Unpaid'
    ])

    return response

@login_required(login_url='login')
def download_mill_record(request, pk):
    mill_record = MillsRecord.objects.get(pk=pk)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="mill_record_{mill_record.pk}.txt"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'KL No', 'Mill Name', 'Mill Place', 'Mill Rate', 'Mill Weight', 'Remarks', 'Mill Amount', 'Rate Type', 'Calculation Type'])
    writer.writerow([
        mill_record.date,
        mill_record.kl_no,
        mill_record.mill_name,
        mill_record.mill_place,
        mill_record.mill_rate,
        mill_record.mill_weight,
        mill_record.mill_remarks,
        mill_record.mill_amount,
        mill_record.mill_rate_type,
        mill_record.mill_calculation_type
    ])
    
    return response

'''from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
@login_required(login_url='login')
def download_mill_record(request, pk):
    mill_record = MillsRecord.objects.get(pk=pk)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="mill_record_{mill_record.pk}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
       # Create vertical data table
    \'''data = [
        ['Field', 'Value'],
        ['Date', str(mill_record.date)],
        ['KL No', mill_record.kl_no],
        ['Mill Name', mill_record.mill_name],
        ['Mill Place', mill_record.mill_place],
        ['Mill Rate', str(mill_record.mill_rate)],
        ['Mill Weight', str(mill_record.mill_weight)],
        ['Remarks', mill_record.mill_remarks],
        ['Mill Amount', str(mill_record.mill_amount)],
        ['Rate Type', mill_record.mill_rate_type],
        ['Calculation Type', mill_record.mill_calculation_type]
    ]\'''
    data = [
        ['Date', 'KL No', 'Mill Name', 'Mill Place', 'Mill Rate', 'Mill Weight', 'Remarks', 'Mill Amount', 'Rate Type', 'Calculation Type'],
        [
            str(mill_record.date),
            mill_record.kl_no,
            mill_record.mill_name,
            mill_record.mill_place,
            str(mill_record.mill_rate),
            str(mill_record.mill_weight),
            mill_record.mill_remarks,
            str(mill_record.mill_amount),
            mill_record.mill_rate_type,
            mill_record.mill_calculation_type
        ]
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    doc.build(elements)
    return response
'''

@login_required(login_url='login')
def youtube(request):
    return render(request,'youtube/youtube.html')

@login_required(login_url='login')
def calculator(request):
    return render(request,'calculator/calculator.html')

def delete_mills_record(request, id):
    mill_record = get_object_or_404(MillsRecord, id=id)
    mill_record.delete()
    return redirect('mills')

def delete_party_record(request, id):
    party_record = get_object_or_404(PartyRecord, id=id)
    party_record.delete()
    return redirect('party')


def error_404(request, exception):
    return render(request, '404_page.html')         
def snakegame(request):
    return render(request,'snake game/index.html')