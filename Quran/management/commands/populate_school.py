from django.core.management.base import BaseCommand
from Quran.models import School, Student, Teacher, Course, ClassGroup, Attendance, Invoice
from django.utils import timezone
import random
from datetime import timedelta
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with dummy school data'

    def handle(self, *args, **kwargs):
        # -------------------------
        # Create a school
        # -------------------------
        school, _ = School.objects.get_or_create(
            name="Green Valley School",
            code="GV001",
            is_active=True
        )

        # -------------------------
        # Create Teachers
        # -------------------------
        teachers = []
        existing_ids = set()
        for _ in range(5):
            while True:
                id_number = str(fake.random_number(digits=14, fix_len=True))
                if id_number not in existing_ids:
                    existing_ids.add(id_number)
                    break

            teacher = Teacher.objects.create(
                school=school,
                id_number=id_number,
                name=fake.name(),
                gender=random.choice(['M', 'F']),
                email=fake.email(),
                phone=fake.phone_number()[:11].replace('-', '').replace(' ', ''),
                birth_date=fake.date_of_birth(minimum_age=25, maximum_age=50),
                is_active=True
            )
            teachers.append(teacher)

        # -------------------------
        # Create Courses
        # -------------------------
        courses = []
        for _ in range(3):
            course = Course.objects.create(
                school=school,
                name=fake.word().capitalize(),
                price=random.randint(100, 500),
                description=fake.text(max_nb_chars=100),
                is_active=True
            )
            courses.append(course)

        # -------------------------
        # Create ClassGroups
        # -------------------------
        groups = []
        for i in range(4):
            group = ClassGroup.objects.create(
                school=school,
                name=f"Group {i+1}",
                teacher=random.choice(teachers),
                course=random.choice(courses),
                is_active=True,
                start_time=timezone.now().time(),
                end_time=(timezone.now() + timedelta(hours=1)).time()
            )
            groups.append(group)

        # -------------------------
        # Create Students
        # -------------------------
        for _ in range(10):
            Student.objects.create(
                school=school,
                name=fake.name(),
                code=str(fake.random_number(digits=5, fix_len=True)),
                phone=fake.phone_number()[:11].replace('-', '').replace(' ', ''),
                gender=random.choice(['M', 'F']),
                birth_date=fake.date_of_birth(minimum_age=10, maximum_age=18),
                academic_year=random.choice([
                    'pre_primary','primary_1','primary_2','primary_3','primary_4',
                    'primary_5','primary_6','middle_1','middle_2','middle_3',
                    'high_1','high_2','high_3','university_1','university_2',
                    'university_3','university_4'
                ]),
                is_active=True,
                registration_date=timezone.now(),
                group=random.choice(groups)
            )

        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))
