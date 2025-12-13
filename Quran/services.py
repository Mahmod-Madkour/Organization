
from Quran.models import Student


def handle_academic_year():
    ACADEMIC_YEAR_UPGRADE = {
        'pre_primary': 'primary_1',
        'primary_1': 'primary_2',
        'primary_2': 'primary_3',
        'primary_3': 'primary_4',
        'primary_4': 'primary_5',
        'primary_5': 'primary_6',
        'primary_6': 'middle_1',
        'middle_1': 'middle_2',
        'middle_2': 'middle_3',
        'middle_3': 'high_1',
        'high_1': 'high_2',
        'high_2': 'high_3',
        'high_3': 'university_1',
        'university_1': 'university_2',
        'university_2': 'university_3',
        'university_3': 'university_4',
        'university_4': 'graduate',
        'graduate': 'graduate',
    }
    students = Student.objects.all()
    for student in students:
        current_year = student.academic_year
        next_year = ACADEMIC_YEAR_UPGRADE.get(current_year)
        if next_year:
            student.academic_year = next_year
            student.save()
        else:
            pass
