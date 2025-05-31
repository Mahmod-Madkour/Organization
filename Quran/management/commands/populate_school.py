from Quran.models import Student, Teacher, Course, Group, Attendance, Invoice
from django.utils import timezone
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Create Teachers
teachers = []
for _ in range(5):
    teacher = Teacher.objects.create(
        name=fake.name(),
        gender=random.choice(['M', 'F']),
        email=fake.email(),
        phone=fake.phone_number()[:11].replace('-', '').replace(' ', ''),
        birth_date=fake.date_of_birth(minimum_age=25, maximum_age=50),
        is_active=True
    )
    teachers.append(teacher)

# Create Courses
courses = []
for _ in range(3):
    course = Course.objects.create(
        name=fake.word().capitalize(),
        price=random.randint(100, 500),
        description=fake.text(max_nb_chars=100),
        is_active=True
    )
    courses.append(course)

# Create Groups
groups = []
for i in range(4):
    group = Group.objects.create(
        name=f"Group {i+1}",
        teacher=random.choice(teachers),
        course=random.choice(courses),
        is_active=True,
        start_time=timezone.now().time(),
        end_time=(timezone.now() + timedelta(hours=1)).time()
    )
    groups.append(group)

# Create Students
for _ in range(10):
    Student.objects.create(
        name=fake.name(),
        code=str(fake.random_number(digits=5, fix_len=True)),
        phone=fake.phone_number()[:11].replace('-', '').replace(' ', ''),
        gender=random.choice(['M', 'F']),
        birth_date=fake.date_of_birth(minimum_age=10, maximum_age=18),
        academic_year=random.choice(['2023/2024', '2024/2025']),
        is_active=True,
        registration_date=timezone.now(),
        group=random.choice(groups)
    )

print("Dummy data created successfully!")
