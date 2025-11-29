from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect, render
from django.urls import path, reverse
from datetime import timedelta
from Quran.models import (
    School,
    Student,
    Teacher,
    Course,
    ClassGroup,
    Invoice,
    Attendance,
    StudentPaymentStatus,
    DiscountConfig,
)


class SchoolInline(admin.TabularInline):
    model = School.users.through
    extra = 1

class CustomUserAdmin(UserAdmin):
    inlines = [SchoolInline]
    list_display = UserAdmin.list_display + ('get_schools',)

    def get_schools(self, obj):
        return ", ".join([school.name for school in obj.schools.all()])
    get_schools.short_description = "Schools"


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    list_filter = ("name", "code", "is_active")
    search_fields = ("name", "code", "is_active")
    ordering = ("name",)
    list_per_page = 25


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "phone", "gender", "academic_year", "group", "is_active", "registration_date")
    list_filter = ("gender", "academic_year", "group", "is_active")
    search_fields = ("name", "code", "phone")
    ordering = ("name",)
    list_per_page = 25
    readonly_fields = ("code", "registration_date")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "gender", "is_active", "registration_date")
    list_filter = ("gender", "is_active")
    search_fields = ("name", "phone", "email")
    ordering = ("name",)
    list_per_page = 25
    readonly_fields = ("registration_date",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 25


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "teacher", "start_time", "end_time", "is_active")
    list_filter = ("course", "teacher", "is_active")
    search_fields = ("name", "course__name", "teacher__name")
    ordering = ("name",)
    list_per_page = 25


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("student", "month", "year", "amount", "date")
    list_filter = ("year", "month")
    search_fields = ("student__name", "student__code")
    date_hierarchy = "date"
    ordering = ("-date",)
    list_per_page = 25


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "date", "present")
    list_filter = ("date", "present")
    search_fields = ("student__name", "student__code")
    date_hierarchy = "date"
    ordering = ("-date",)
    list_per_page = 25


@admin.register(StudentPaymentStatus)
class StudentPaymentStatusAdmin(admin.ModelAdmin):
    list_display = ("student", "month", "year", "is_paid")
    list_filter = ("is_paid", "year", "month")
    search_fields = ("student__name", "student__code")
    ordering = ("-year", "-month")
    list_per_page = 25


@admin.register(DiscountConfig)
class DiscountConfigAdmin(admin.ModelAdmin):
    list_display = ('school', 'name', 'value', 'updated_at')
    list_filter = ('school',)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)