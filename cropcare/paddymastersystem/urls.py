
from django.urls import path
from . import views

urlpatterns = [
    path('create_record/', views.create_record, name='create_record'),
    path('record_details/', views.record_details, name='record_details'),
    path('common/', views.common, name='common'),
    path('party/', views.party, name='party'),
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('interest_entry/', views.interest_entry, name='interest_entry'),
    path('success/', views.success, name='success'),
    path('view_credits/', views.view_credits, name='view_credits'),
    path('view_debits/', views.view_debits, name='view_debits'),
    path('mills/', views.mills, name='mills'),
    path('party/<int:pk>/', views.party_detail_view, name='party_detail_view'), 
    path('mills/<int:pk>/', views.mills_detail_view, name='mills_detail_view'),
    path('party/<int:pk>/', views.party_detail_view, name='party_detail_view'),
    path('add_mill_record/', views.add_mill_record, name='add_mill_record'),
    path('add_party_record/', views.add_party_record, name='add_party_record'),
    path('download_pl_report/', views.download_pl_report, name='download_pl_report'),  # Assuming you have a download view
    path('search_party/', views.search_records_party, name='search_records_party'),
    path('search_mills/', views.search_records_mills, name='search_records_mills'),
    path('search_pnl/', views.search_records_pnl, name='search_records_pnl'),
    path('search_ledger/', views.search_records_ledger, name='search_records_ledger'),
    path('logout/', views.logout_view, name='logout'),
    path('ledger/', views.ledger, name='ledger'),
    path('ledger/add/', views.add_ledger_entry, name='add_ledger_entry'),
    path('ledger/delete/<int:entry_id>/', views.delete_ledger_entry, name='delete_ledger_entry'),
    path('ledger/edit/<int:pk>/', views.edit_ledger_entry, name='edit_ledger_entry'),
    path('ledger/view/', views.view_ledger, name='view_ledger'),
    path('view/', views.view_records, name='view_records'),
    path('party-record/<int:pk>/edit/', views.edit_party_record, name='edit_party_record'),
    path('mills-record/<int:pk>/edit/', views.edit_mills_record, name='edit_mills_record'),
    path('download_ledger_csv/', views.download_ledger_csv, name='download_ledger_csv'),
    path('download_party_record_details/<int:pk>/', views.download_party_record_details, name='download_party_record_details'),
    path('download_mill_record/<int:pk>/', views.download_mill_record, name='download_mill_record'),
    path('homepage/', views.homepage, name='homepage'),
    path('youtube/', views.youtube, name='youtube'),
    path('calculator/', views.calculator, name='calculator'),
    path('delete_mills/<int:id>/', views.delete_mills_record, name='delete_mills_record'),
    path('delete_party/<int:id>/', views.delete_party_record, name='delete_party_record'),
    path('delete_credit/<int:entry_id>/', views.delete_credit, name='delete_credit'),
    path('delete_debit/<int:entry_id>/', views.delete_debit, name='delete_debit'),
    path('enter-otp/', views.enter_otp, name='enter_otp'),
    path('adminregister/', views.adminregister, name='adminregister'),
    path('snakegame/', views.snakegame, name='snakegame'),

]

   

