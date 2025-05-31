import random
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.validators import MinValueValidator, ValidationError, RegexValidator


GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
]

ACADEMIC_YEAR_CHOICES = [
    ('pre_primary', 'Pre-Primary'),
    ('primary_1', 'Primary 1'),
    ('primary_2', 'Primary 2'),
    ('primary_3', 'Primary 3'),
    ('primary_4', 'Primary 4'),
    ('primary_5', 'Primary 5'),
    ('primary_6', 'Primary 6'),
    ('middle_1', 'Middle 1'),
    ('middle_2', 'Middle 2'),
    ('middle_3', 'Middle 3'),
    ('high_1', 'High 1'),
    ('high_2', 'High 2'),
    ('high_3', 'High 3'),
    ('university_1', 'University Year 1'),
    ('university_2', 'University Year 2'),
    ('university_3', 'University Year 3'),
    ('university_4', 'University Year 4'),
]

phone_regex = RegexValidator(
    regex=r'^\d{11}$',
    message="Phone number must be exactly 11 digits and contain only numbers."
)


class Student(models.Model):
    name = models.CharField(max_length=100, verbose_name="Student Name")
    code = models.CharField(max_length=5, unique=True, blank=True)
    phone = models.CharField(max_length=11, validators=[phone_regex], verbose_name="Phone Number")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Birth Date")
    academic_year = models.CharField(max_length=100, blank=True, null=True,  choices=ACADEMIC_YEAR_CHOICES, verbose_name="Academic Year")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    registration_date = models.DateTimeField(default=timezone.now)
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name="Group", blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
    def save(self, *args, **kwargs):
        # Create code for student
        if not self.code:
            self.code = self.generate_unique_code()        
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        first_digit = 1
        while True:
            code = f"{first_digit}{random.randint(1000, 9999)}"
            if not Student.objects.filter(code=code).exists():
                return code

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Teacher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Teacher Name")
    phone = models.CharField(max_length=11, validators=[phone_regex], verbose_name="Phone Number")
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="Email")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Birth Date")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Course Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Price")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Active")

    def __str__(self):
        return f"{self.name} - {self.price}"

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Group(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey('Course', on_delete=models.PROTECT, related_name='groups')
    teacher = models.ForeignKey('Teacher', on_delete=models.PROTECT, related_name='groups')
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        formatted_start = self.start_time.strftime('%-I:%M %p')
        formatted_end = self.end_time.strftime('%-I:%M %p')
        return f"{self.name} - From: {formatted_start} To: {formatted_end}"
    
    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class Invoice(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='invoices')
    date = models.DateField(default=timezone.now, verbose_name="Date")
    month = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Month")
    year = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Year")
    amount = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Total Amount")

    def __str__(self):
        return f"Invoice for {self.student.name}"

    def clean(self):
        super().clean()
        group = self.student.group
        if not group:
            raise ValidationError("Student is not assigned to any group.")

        expected_price = group.course.price
        if self.amount != expected_price:
            raise ValidationError(f'The amount {self.amount} must equal course price {expected_price}.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        StudentPaymentStatus.objects.update_or_create(
            invoice=self,
            student=self.student,
            month=self.month,
            year=self.year,
            is_paid=True
        )

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        unique_together = ('student', 'month', 'year')


class Attendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    present = models.BooleanField(default=True)

    class Meta:
        unique_together = ('date', 'student')
        ordering = ['-date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    def __str__(self):
        return f"{self.student.name} on {self.date} - {'Present' if self.present else '-'}"


class StudentPaymentStatus(models.Model):
    invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, related_name='payments')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='payment_status')
    month = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Month")
    year = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Year")
    is_paid = models.BooleanField(default=False, verbose_name="Paid this Month")

    def __str__(self):
        return f"Payment status for {self.student.name} - {self.month}/{self.year}"

    class Meta:
        verbose_name = "Student Payment Status"
        verbose_name_plural = "Student Payment Statuses"
        unique_together = ('student', 'month', 'year')
