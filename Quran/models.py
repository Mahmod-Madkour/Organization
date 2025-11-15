import random
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, RegexValidator, ValidationError

# -------------------------
# Validators
# -------------------------

id_regex = RegexValidator(regex=r'^\d{14}$', message=_("ID number must be exactly 14 digits."))
phone_regex = RegexValidator(regex=r'^\d{11}$', message=_("Phone number must be exactly 11 digits."))

# -------------------------
# Choices
# -------------------------

GENDER_CHOICES = [
    ('M', _('Male')),
    ('F', _('Female'))
]

ACADEMIC_YEAR_CHOICES = [
    ('pre_primary', _('Pre-Primary')),
    ('primary_1', _('Primary 1')),
    ('primary_2', _('Primary 2')),
    ('primary_3', _('Primary 3')),
    ('primary_4', _('Primary 4')),
    ('primary_5', _('Primary 5')),
    ('primary_6', _('Primary 6')),
    ('middle_1', _('Middle 1')),
    ('middle_2', _('Middle 2')),
    ('middle_3', _('Middle 3')),
    ('high_1', _('High 1')),
    ('high_2', _('High 2')),
    ('high_3', _('High 3')),
    ('university_1', _('University Year 1')),
    ('university_2', _('University Year 2')),
    ('university_3', _('University Year 3')),
    ('university_4', _('University Year 4')),
]

# -------------------------
# Models
# -------------------------

class School(models.Model):
    users = models.ManyToManyField(User, blank=True, related_name='schools')
    name = models.CharField(max_length=255, verbose_name=_("School Name"))
    code = models.CharField(max_length=50, unique=True, verbose_name=_("School Code"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")


class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachers')
    id_number = models.CharField(max_length=14, validators=[id_regex], unique=True, verbose_name=_("ID"))
    name = models.CharField(max_length=100, verbose_name=_("Teacher Name"))
    phone = models.CharField(max_length=11, validators=[phone_regex], verbose_name=_("Phone Number"))
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name=_("Email"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_("Gender"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Birth Date"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    registration_date = models.DateTimeField(default=timezone.now, verbose_name=_("Registration Date"))

    def __str__(self):
        return self.name


class Course(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='courses', verbose_name=_("School"))
    name = models.CharField(max_length=100, verbose_name=_("Course Name"))
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name=_("Price"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        return f"{self.name} - {self.price}"


class ClassGroup(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='class_groups', verbose_name=_("School"))
    name = models.CharField(max_length=50, verbose_name=_("Group Name"))
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='class_groups', verbose_name=_("Course"))
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='class_groups', verbose_name=_("Teacher"))
    start_time = models.TimeField(verbose_name=_("Start Time"))
    end_time = models.TimeField(verbose_name=_("End Time"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        return f"{self.name} ({self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')})"


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students', verbose_name=_("School"))
    name = models.CharField(max_length=100, verbose_name=_("Student Name"))
    code = models.CharField(max_length=5, unique=True, blank=True, verbose_name=_("Code"))
    phone = models.CharField(max_length=11, validators=[phone_regex], verbose_name=_("Phone Number"))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name=_("Gender"))
    birth_date = models.DateField(blank=True, null=True, verbose_name=_("Birth Date"))
    academic_year = models.CharField(max_length=20, choices=ACADEMIC_YEAR_CHOICES, blank=True, null=True, verbose_name=_("Academic Year"))
    group = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='students', verbose_name=_("Group"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    registration_date = models.DateTimeField(default=timezone.now, verbose_name=_("Registration Date"))

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        while True:
            code = str(random.randint(1000, 9999))
            if not Student.objects.filter(code=code).exists():
                return code


class Invoice(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='invoices', verbose_name=_("School"))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='invoices', verbose_name=_("Student"))
    date = models.DateField(default=timezone.now, verbose_name=_("Date"))
    month = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_("Month"))
    year = models.PositiveIntegerField(validators=[MinValueValidator(2000)], verbose_name=_("Year"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name=_("Total Amount"))

    class Meta:
        unique_together = ('student', 'month', 'year')

    def __str__(self):
        return f"Invoice for {self.student.name} - {self.month}/{self.year}"

    def clean(self):
        super().clean()
        if not self.student.group:
            raise ValidationError(_("Student is not assigned to any group."))
        expected_price = self.student.group.course.price
        if self.amount != expected_price:
            raise ValidationError(_(f"The amount {self.amount} must equal course price {expected_price}."))


class Attendance(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='attendances', verbose_name=_("School"))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances', verbose_name=_("Student"))
    date = models.DateField(verbose_name=_("Date"))
    present = models.BooleanField(default=True, verbose_name=_("Present"))

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']


class StudentPaymentStatus(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='student_payment_statuses', verbose_name=_("School"))
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payment_statuses', verbose_name=_("Student"))
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments', verbose_name=_("Invoice"))
    month = models.PositiveIntegerField(verbose_name=_("Month"))
    year = models.PositiveIntegerField(verbose_name=_("Year"))
    is_paid = models.BooleanField(default=False, verbose_name=_("Paid"))

    class Meta:
        unique_together = ('student', 'month', 'year')
