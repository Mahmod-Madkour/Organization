from django import forms
from django.forms.widgets import TimeInput, RadioSelect
from Quran.models import (
    Student, Teacher, Course, Group, GENDER_CHOICES, ACADEMIC_YEAR_CHOICES
)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'phone', 'gender', 'birth_date', 'academic_year', 'group', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'type': 'tel',
                'pattern': r'\d{11}',
                'maxlength': '11',
                'class': 'form-control',
                'placeholder': 'Enter 11-digit phone number'
            }),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select2'}),
            'academic_year': forms.Select(attrs={'class': 'form-select2'}),
            'group': forms.Select(attrs={'class': 'form-select2'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'phone', 'email', 'gender', 'birth_date', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'type': 'tel',
                'pattern': r'\d{11}',
                'maxlength': '11',
                'class': 'form-control',
                'placeholder': 'Enter 11-digit phone number'
            }),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select2'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
