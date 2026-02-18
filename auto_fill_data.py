import os
import django
import pandas as pd
import re
from datetime import datetime, time
from django.db.models import Count

# ==============================
# DJANGO SETUP
# ==============================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Organization.settings")
django.setup()

# ==============================
# DJANGO IMPORTS
# ==============================
from Quran.models import School, Course, Student, Teacher, ClassGroup

# ==============================
# LOAD EXCEL
# ==============================
EXCEL_PATH = "./Data/asheer_students.xlsx"
df = pd.read_excel(
    EXCEL_PATH,
    header=None,
    skiprows=1,
    dtype=str
)
group_values = df.iloc[:, 6].dropna().unique()

# ==============================
# GET SCHOOL & COURSE
# ==============================
school = School.objects.first()
course = Course.objects.first()
if not school or not course:
    raise Exception("School or Course not found")

# ==============================
# HELPERS
# ==============================
ACADEMIC_YEAR_MAP = {
    'الصف الاول الابتدائى': 'primary_1',
    'الصف الثانى الابتدائى': 'primary_2',
    'الصف الثالث الابتدائى': 'primary_3',
    'الصف الرابع الابتدائى': 'primary_4',
    'الصف الخامس الابتدائى': 'primary_5',
    'الصف السادس الابتدائى': 'primary_6',
    'الصف الاول الاعدادى': 'middle_1',
    'الصف الثانى الاعدادى': 'middle_2',
    'الصف الثالث الاعدادى': 'middle_3',
    'الصف الاول الثانوى': 'high_1',
    'الصف الثانى الثانوى': 'high_2',
    'الصف الثالث الثانوى': 'high_3',
    'الفرقة الاولى جامعة': 'university_1',
    'الفرقة الثانية جامعة': 'university_2',
    'الفرقة الثالثة جامعة': 'university_3',
    'الفرقة الرابعة جامعة': 'university_4',
    'خريج': 'graduate',
}

def normalize_name(name):
    name = str(name)
    name = re.sub(r'(الشيخ|شيخ|أ\.|ا\.)', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def normalize_phone(phone_raw):
    if not phone_raw:
        return ''
    phone = str(phone_raw).strip()
    phone = re.sub(r"\D", "", phone)

    # Fix Egyptian 10-digit mobile numbers
    if len(phone) == 10 and not phone.startswith("0"):
        phone = "0" + phone

    return phone

def normalize_gender(gender_raw):
    gender = str(gender_raw).strip()
    if gender in ['أنثى', 'انثى', 'و', 'ف']:
        return 'F'
    if gender in ['ذكر', 'م', 'ذ']:
        return 'M'
    return None

def parse_birth_date(value):
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.date()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, (int, float)):
        return (pd.to_datetime('1899-12-30') + pd.to_timedelta(value, unit='D')).date()
    if isinstance(value, str):
        for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(value.strip(), fmt).date()
            except ValueError:
                continue
    return None

def parse_arabic_time(t):
    t = t.strip()
    is_pm = 'م' in t
    is_am = 'ص' in t
    t = t.replace('م', '').replace('ص', '').strip()
    hour, minute = map(int, t.split(':'))
    if is_pm and hour != 12: hour += 12
    if is_am and hour == 12: hour = 0
    return time(hour, minute)

def extract_name_and_time(text):
    DEFAULT_START = time(13, 0)
    DEFAULT_END = time(15, 0)

    text = str(text).strip()
    match = re.search(r'(\d{1,2}:\d{2}\s*[مص])\s*-\s*(\d{1,2}:\d{2}\s*[مص])', text)

    start_time = parse_arabic_time(match.group(1)) if match else DEFAULT_START
    end_time = parse_arabic_time(match.group(2)) if match else DEFAULT_END

    name = re.sub(r'\(.*?\)', '', text)
    return normalize_name(name), start_time, end_time

# UNIQUE ID HANDLING
existing_ids = set(
    Student.objects.filter(school=school).values_list("id_number", flat=True)
)
used_ids_in_file = set()

def generate_unique_fallback_id():
    while True:
        new_id = "9" + str(int(pd.Timestamp.now().timestamp() * 1000000))[-13:]
        if new_id not in existing_ids and new_id not in used_ids_in_file:
            return new_id

# ==============================
# CREATE TEACHERS & CLASSGROUPS
# ==============================
teachers_cache = {}

for cell in group_values:
    teacher_name, start_time, end_time = extract_name_and_time(cell)
    if not teacher_name: 
        continue

    teacher = teachers_cache.get(teacher_name)
    if not teacher:
        teacher = Teacher.objects.filter(school=school, name__iexact=teacher_name).first()
        if not teacher:
            teacher = Teacher.objects.create(
                school=school,
                name=teacher_name,
                id_number=str(pd.Timestamp.now().timestamp()).replace('.', '')[:14],
                phone="01000000000",
                gender="M",
                marital_status="S",
                qualification="Quran Teacher",
            )
        teachers_cache[teacher_name] = teacher

    ClassGroup.objects.get_or_create(
        school=school,
        course=course,
        teacher=teacher,
        start_time=start_time,
        end_time=end_time,
        defaults={
            "name": f"{teacher_name} ({start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')})"
        }
    )

print("✅ Teachers and ClassGroups created successfully")

# ==============================
# DELETE ONLY STUDENTS WITHOUT RELATIONS
# ==============================

students_to_delete = (
    Student.objects
    .filter(school=school)
    .annotate(
        invoice_count=Count('invoices'),
        attendance_count=Count('attendances'),
        payment_status_count=Count('payment_statuses')
    )
    .filter(
        invoice_count=0,
        attendance_count=0,
        payment_status_count=0
    )
)

deleted_count, _ = students_to_delete.delete()

print(f"🗑 Deleted {deleted_count} students without relations")

# ==============================
# CREATE STUDENTS
# ==============================

students_created = 0
students_updated = 0
rows_with_issues = []

for idx, row in df.iterrows():
    # Extract raw values
    name = row[0];
    id_number = row[1];
    gender_raw = row[2]
    birth_date_raw = row[3];
    academic_year_raw = row[4];
    level = row[5]
    group_cell = row[6];
    phone_raw = row[7];
    phone_raw_2 = row[8];
    parent_profession = row[9];
    discount_flag = row[10]

    missing_cols = []

    # NAME
    if pd.isna(name) or str(name).strip() == "":
        name = f"UNKNOWN_{idx+2}"
        missing_cols.append("name")
    else:
        name = str(name).strip()

    # ID NUMBER
    id_number = str(id_number).strip() if id_number else ""
    id_number = re.sub(r"\D", "", id_number)

    if len(id_number) != 14:
        id_number = generate_unique_fallback_id()
        missing_cols.append("id_number")

    if id_number in existing_ids or id_number in used_ids_in_file:
        id_number = generate_unique_fallback_id()
        missing_cols.append("duplicate_id")

    used_ids_in_file.add(id_number)

    # GENDER (Default M)
    gender = normalize_gender(gender_raw)
    if not gender:
        gender = "M"
        missing_cols.append("gender")

    # BIRTH DATE
    birth_date = parse_birth_date(birth_date_raw)
    if not birth_date:
        birth_date = datetime(2026, 1, 1).date()
        missing_cols.append("birth_date")

    # ACADEMIC YEAR
    academic_year = ACADEMIC_YEAR_MAP.get(
        str(academic_year_raw).strip()
    ) if not pd.isna(academic_year_raw) else None

    if not academic_year:
        academic_year = "pre_primary"
        missing_cols.append("academic_year")

    # LEVEL
    if pd.isna(level) or str(level).strip() == "":
        level = "غير محدد"
        missing_cols.append("level")
    else:
        level = str(level).strip()

    # PHONE
    phone = normalize_phone(phone_raw)
    if not phone:
        phone = "00000000000"
        missing_cols.append("phone")

    # PARENT PROFESSION
    if pd.isna(parent_profession) or str(parent_profession).strip() == "":
        parent_profession = "غير محدد"
        missing_cols.append("parent_profession")
    else:
        parent_profession = str(parent_profession).strip()

    # GROUP
    teacher_name, start_time, end_time = extract_name_and_time(group_cell)

    class_group = ClassGroup.objects.filter(
        school=school,
        teacher__name__iexact=teacher_name,
        start_time=start_time,
        end_time=end_time
    ).first()

    if not class_group:
        missing_cols.append("group_not_found")
        class_group = ClassGroup.objects.first()

    # DISCOUNT
    discount_type = 'discount' if str(discount_flag).strip() == 'نعم' else 'none'
    if pd.isna(discount_flag):
        missing_cols.append("discount_flag")

    # =============================
    # CREATE OR UPDATE
    # =============================
    student, created = Student.objects.update_or_create(
        school=school,
        id_number=id_number,
        defaults={
            'name': name,
            'gender': gender,
            'birth_date': birth_date,
            'academic_year': academic_year,
            'level': level,
            'group': class_group,
            'phone': phone,
            'parent_profession': parent_profession,
            'discount_type': discount_type,
            'is_active': True,
        }
    )

    if created:
        students_created += 1
    else:
        students_updated += 1

    # Log issues
    if missing_cols:
        rows_with_issues.append({
            "row": idx + 2,
            "student_name": name,
            "missing": missing_cols
        })

# ==============================
# REPORT
# ==============================
print(f"\n✅ Students created: {students_created}")
print(f"♻️ Students updated: {students_updated}")

if rows_with_issues:
    print("\n⚠️ Rows with auto-filled defaults:\n")
    for issue in rows_with_issues:
        print(
            f"Row {issue['row']} | "
            f"Name: {issue['student_name']} | "
            f"Defaulted: {', '.join(issue['missing'])}"
        )
else:
    print("✅ No missing values detected.")
