from django.contrib import admin
from .models import Student, Teacher, Course, Invoice


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    fields = ('name', 'gender', 'phone', 'birth_date', 'is_active')
    list_display = ('name', 'gender', 'phone', 'is_active')
    list_filter = ('gender', 'is_active')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    fields = ('name', 'gender', 'phone', 'email', 'birth_date', 'is_active')
    list_display = ('name', 'phone', 'is_active')
    list_filter = ('name', 'phone', 'is_active')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('name', 'is_active')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount', 'payment_date', 'month', 'year')
    list_filter = ('student', 'payment_date', 'month', 'year')
