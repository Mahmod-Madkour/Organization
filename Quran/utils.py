from datetime import date
from Quran.models import School, Attendance, StudentPaymentStatus


def get_user_school(request):
    user = request.user
    if user.is_superuser:
        return School.objects.all()
    else:
        return School.objects.filter(users=user)


def get_present_for_student(student_id, selected_date):
    attendance = Attendance.objects.filter(student_id=student_id, date=selected_date).first()
    return attendance.present if attendance else False


def get_missing_months_for_student(student_id):
    start_year, start_month = 2026, 1
    today = date.today()

    required_months = []
    y, m = start_year, start_month
    while (y < today.year) or (y == today.year and m <= today.month):
        required_months.append((y, m))
        m += 1
        if m > 12:
            m, y = 1, y + 1

    existing_months = set(
        StudentPaymentStatus.objects.filter(student_id=student_id).values_list('year', 'month')
    )

    return [
        f"{year}-{month:02d}"
        for (year, month) in required_months
        if (year, month) not in existing_months
    ]