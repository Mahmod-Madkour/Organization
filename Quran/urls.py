from django.urls import path, include
from Quran.views import home, attendance, create_invoice, print_invoice

urlpatterns = [
    path('', home, name='home'),
    path('attendance/', attendance, name='attendance'),
    path('invoice/create/', create_invoice, name='create_invoice'),
    path('invoice/print/<int:invoice_id>/', print_invoice, name='print_invoice'),
]
