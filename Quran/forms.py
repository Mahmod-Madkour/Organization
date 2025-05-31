from django import forms
from django.forms.widgets import TimeInput, RadioSelect
from Quran.models import Student, Teacher, Course, Group, GENDER_CHOICES, ACADEMIC_YEAR_CHOICES


class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'style': (
                'border: 1px solid #ced4da; '
                'border-radius: 4px; '
                'padding: 6px 12px; '
                'width: 250px; '
                'box-shadow: none;'
            )
        }),
        required=False
    )
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES,
        widget=RadioSelect(attrs={'style': 'display: inline; margin-right: 20px;'}),
        required=True
    )
    academic_year = forms.ChoiceField(
        choices=ACADEMIC_YEAR_CHOICES,
        widget=forms.Select(attrs={'class': 'select2', 'style': 'width: 275px !important;'}),
        required=False
    )
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'style': 'width: 500px !important;'}),
        required=False
    )

    class Media:
        css = {
            'all': ('css/select2.min.css',)
        }
        js = (
            'js/jquery.min.js',
            'js/select2.min.js',
            'admin/js/custom_select2.js',
        )


class TeacherAdminForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'style': (
                'border: 1px solid #ced4da; '
                'border-radius: 4px; '
                'padding: 6px 12px; '
                'width: 200px; '
                'box-shadow: none;'
            )
        }),
        required=False
    )
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES,
        widget=RadioSelect(attrs={'style': 'display: inline; margin-right: 20px;'}),
        required=True
    )


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'style': 'width: 400px !important;'})
    )
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        widget=forms.Select(attrs={'class': 'select2', 'style': 'width: 400px !important;'})
    )
    start_time = forms.TimeField(
        widget=TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
            'required': 'required',
            'style': (
                'border: 1px solid #ced4da; '
                'border-radius: 4px; '
                'padding: 6px 12px; '
                'width: 200px; '
                'box-shadow: none;'
            )
        })
    )
    end_time = forms.TimeField(
        widget=TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
            'required': 'required',
            'style': (
                'border: 1px solid #ced4da; '
                'border-radius: 4px; '
                'padding: 6px 12px; '
                'width: 200px; '
                'box-shadow: none;'
            )        })
    )

    class Media:
        css = {
            'all': ('css/select2.min.css',)
        }
        js = (
            'js/jquery.min.js',
            'js/select2.min.js',
            'admin/js/custom_select2.js',
        )
