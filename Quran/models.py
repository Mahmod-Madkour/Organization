from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone


class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=100, verbose_name="Student Name")
    phone = models.CharField(max_length=11, verbose_name="Phone Number")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Birth Date")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"


class Teacher(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=100, verbose_name="Teacher Name")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
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
        return self.name

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"


class Invoice(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='invoices', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='invoices', verbose_name="Course")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Amount")
    payment_date = models.DateTimeField(default=timezone.now)
    month = models.IntegerField(choices=[(i, f'{i:02d}') for i in range(1, 13)], verbose_name="Month")
    year = models.IntegerField(choices=[(i, i) for i in range(2025, 2041)], verbose_name="Year")

    class Meta:
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"

#     def save(self, *args, **kwargs):
#         # حساب تواريخ بداية ونهاية الاشتراك تلقائياً
#         self.subscription_start = date(self.year, self.month, 1)
        
#         if self.month == 12:
#             self.subscription_end = date(self.year + 1, 1, 1) - timedelta(days=1)
#         else:
#             self.subscription_end = date(self.year, self.month + 1, 1) - timedelta(days=1)
            
#         super().save(*args, **kwargs)

# class Group(models.Model):
#     name = models.CharField(max_length=50)
#     course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='groups')
#     teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name='groups')
#     start_date = models.DateField()
#     end_date = models.DateField()
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.name} - {self.course.name}"

#     class Meta:
#         verbose_name = "مجموعة"
#         verbose_name_plural = "المجموعات"
#         constraints = [
#             CheckConstraint(
#                 check=Q(end_date__gt=F('start_date')),
#                 name='check_group_dates'
#             )
#         ]


# class Group(models.Model):
#     name = models.CharField(max_length=50, verbose_name="اسم المجموعة")
#     course = models.ForeignKey('Course', on_delete=models.PROTECT, related_name='groups', verbose_name="الكورس")
#     teacher = models.ForeignKey('Teacher', on_delete=models.PROTECT, related_name='groups', verbose_name="المدرس")
#     max_capacity = models.PositiveIntegerField(default=50, validators=[MinValueValidator(1), MaxValueValidator(100)], verbose_name="الحد الأقصى للطلاب")
#     start_time = models.TimeField(verbose_name="وقت البدء")
#     end_time = models.TimeField(verbose_name="وقت الانتهاء")

#     def __str__(self):
#         return f"{self.name} - {self.course.name}"

#     class Meta:
#         verbose_name = "مجموعة"
#         verbose_name_plural = "المجموعات"
#         constraints = [
#             CheckConstraint(
#                 check=Q(end_time__gt=F('start_time')),
#                 name='check_group_times'
#             )
#         ]


# class StudentGroup(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.PROTECT, related_name='groups', verbose_name="الجروب")
#     students = models.ForeignKey('Student', related_name='student_groups', verbose_name="الطلاب المشتركين")


# class Attendance(models.Model):
#     STATUS_CHOICES = [
#         ('present', 'حاضر'),
#         ('absent', 'غائب'),
#     ]
#     year = 
#     month = 
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')

#     def __str__(self):
#         return f"{self.enrollment} - {self.session_date}"

#     class Meta:
#         verbose_name = "حضور"
#         verbose_name_plural = "سجلات الحضور"
#         unique_together = ('enrollment', 'session_date')

