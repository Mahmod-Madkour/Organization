from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, reverse
from datetime import timedelta
from Quran.models import Student, Teacher, Course, Group, Attendance, Invoice
from Quran.forms import StudentAdminForm, TeacherAdminForm, GroupAdminForm
from Quran.views import attendance, create_invoice


# Student
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ('name', 'code', 'gender', 'phone', 'group', 'is_active')
    list_filter = ('code', 'gender', 'is_active')

    fieldsets = (
        ('Personal Info', {'fields': ('name', 'code', 'phone', 'gender')}),
        ('Advanced Options', {'fields': ('birth_date', 'academic_year', 'is_active')}),
        ('Group', {'fields': ('group',)}),
    )

    def get_readonly_fields(self, request, obj=None):
        return ['code']


# Teacher
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm
    list_display = ('name', 'gender', 'phone', 'is_active')
    list_filter = ('name', 'gender', 'phone', 'is_active')

    fieldsets = (
        ('Personal Info', {'fields': ('name', 'gender', 'email', 'phone'), }),
        ('Advanced Options', {'fields': ('birth_date', 'is_active'),}),
    )

# Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active')
    list_filter = ('name', 'is_active')

    fieldsets = (
        ('Course Info', {'fields': ('name', 'price', 'is_active')}),
        ('Details', {'fields': ('description',)}),
    )

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    list_display = ('name', 'teacher', 'course', 'start_time', 'end_time')
    list_filter = ('name', 'teacher', 'course')
    fieldsets = (
        ('Group Info', {'fields': ('name', 'is_active')}),
        ('Details', {'fields': ('course', 'teacher')}),
        ('Timing', {'fields': ('start_time', 'end_time')}),
    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect('admin:attendance-admin-view') 

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(attendance), name='attendance'),
        ]
        return custom_urls + urls

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        return redirect('admin:invoice-admin-view') 

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(create_invoice), name='create-invoice'),
        ]
        return custom_urls + urls
