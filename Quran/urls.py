from django.urls import path, include
from Quran.views import (
    HomeView,
    StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView,
    TeacherListView, TeacherCreateView, TeacherUpdateView, TeacherDeleteView,
    CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    ClassGroupListView, ClassGroupCreateView, ClassGroupUpdateView, ClassGroupDeleteView,
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

    # Course
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/add/', CourseCreateView.as_view(), name='course_add'),
    path('courses/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),

    # Course
    path('class_groups/', ClassGroupListView.as_view(), name='class_group_list'),
    path('class_groups/add/', ClassGroupCreateView.as_view(), name='class_group_add'),
    path('class_groups/<int:pk>/edit/', ClassGroupUpdateView.as_view(), name='class_group_edit'),
    path('class_groups/<int:pk>/delete/', ClassGroupDeleteView.as_view(), name='class_group_delete'),

    # Attendance
    path('attendance/', AttendanceView.as_view(), name='attendance'),

    # Invoice
    path('invoice/', InvoiceCreateView.as_view(), name='invoice'),
    path('invoice/print/<int:invoice_id>/', print_invoice, name='print_invoice'),
]
