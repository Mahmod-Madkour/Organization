from django.urls import path, include
from Quran.views import (
    HomeView,
    StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView,
    TeacherListView, TeacherCreateView, TeacherUpdateView, TeacherDeleteView,
    AttendanceView,
    InvoiceCreateView, print_invoice

)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # Student
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/add/', StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/edit/', StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),

    # Teacher
    path('teachers/', TeacherListView.as_view(), name='teacher_list'),
    path('teachers/add/', TeacherCreateView.as_view(), name='teacher_add'),
    path('teachers/<int:pk>/edit/', TeacherUpdateView.as_view(), name='teacher_edit'),
    path('teachers/<int:pk>/delete/', TeacherDeleteView.as_view(), name='teacher_delete'),

    # Teacher
    path('attendance/', AttendanceView.as_view(), name='attendance'),

    # Invoice
    path('invoice/', InvoiceCreateView.as_view(), name='invoice'),
    path('invoice/print/<int:invoice_id>/', print_invoice, name='print_invoice'),
]
