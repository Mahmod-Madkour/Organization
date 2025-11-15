from django import forms
from django.forms.widgets import TimeInput, RadioSelect
from Quran.models import (
    Student, Teacher, Course, ClassGroup, GENDER_CHOICES, ACADEMIC_YEAR_CHOICES
)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['school', 'name', 'phone', 'gender', 'birth_date', 'academic_year', 'group', 'is_active']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-select2'}),
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not (user and user.is_superuser):
            self.fields.pop('school')

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['school', 'name', 'id_number', 'phone', 'email', 'gender', 'birth_date', 'is_active']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-select2'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={
                'type': 'number',
                'pattern': r'\d{14}',
                'maxlength': '14',
                'class': 'form-control',
                'placeholder': 'Enter 14-digit ID'
            }),
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not (user and user.is_superuser):
            self.fields.pop('school')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['school', 'name', 'price', 'description', 'is_active']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-select2'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'type': 'number', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not (user and user.is_superuser):
            self.fields.pop('school')


class ClassGroupForm(forms.ModelForm):
    class Meta:
        model = ClassGroup
        fields = ['school', 'name', 'course', 'teacher', 'start_time', 'end_time', 'is_active']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-select2'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select2'}),
            'teacher': forms.Select(attrs={'class': 'form-select2'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not (user and user.is_superuser):
            self.fields.pop('school')
