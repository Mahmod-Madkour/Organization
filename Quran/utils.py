import calendar
from datetime import date, datetime
from django.db.models import Count, Q, F, Value, IntegerField, DecimalField, ExpressionWrapper, Case, When
from decimal import Decimal
from Quran.models import (
    School, Attendance, StudentPaymentStatus, Invoice, ClassGroup, DiscountConfig
)


def get_user_school(request):
    user = request.user
    if user.is_superuser:
        return School.objects.all()
    else:
        return School.objects.filter(users=user)


def get_present_for_student(student_id, selected_date):
    attendance = Attendance.objects.filter(student_id=student_id, date=selected_date).first()
    return attendance.present if attendance else True


def get_missing_months_for_student(student):
    if student.discount_type == 'full':
        return []

    start_year, start_month = 2025, 10
    today = date.today()

    required_months = []
    y, m = start_year, start_month
    while (y < today.year) or (y == today.year and m <= today.month):
        required_months.append((y, m))
        m += 1
        if m > 12:
            m, y = 1, y + 1

    existing_months = set(
        StudentPaymentStatus.objects.filter(student_id=student.id).values_list('year', 'month')
    )

    missing_months = []
    for (year, month) in required_months:
        if (year, month) not in existing_months:
            missing_months.append(f"{year}-{month:02d}" )

    return missing_months


def get_group_summary(school_id, month, year):
    # Get start day of month
    date_from = date(year, month, 1)

    # Get last day of month
    last_day = calendar.monthrange(year, month)[1]
    date_to = date(year, month, last_day)

    # Filter invoices by date range
    invoice_qs = Invoice.objects.filter(date__range=(date_from, date_to))

    # Get the discount value for the school, default to 0 if not set
    discount_value = DiscountConfig.objects.filter(school_id=school_id).first()
    discount_amount = discount_value.value if discount_value else Decimal('0.00')

    data = (
        ClassGroup.objects.filter(school_id=school_id)
        .select_related('teacher')
        .annotate(
            total_students=Count('students', distinct=True),
            price=F("course__price"),

            # Paid current month
            students_paid_current=Count(
                'students__payment_statuses',
                filter=Q(
                    students__discount_type='none',
                    students__payment_statuses__is_paid=True,
                    students__payment_statuses__invoice__in=invoice_qs,
                    students__payment_statuses__invoice__month=month,
                    students__payment_statuses__invoice__year=year,
                ),
                distinct=True,
            ),

            # Paid previous months
            students_paid_previous=Count(
                'students__payment_statuses',
                filter=Q(
                    students__discount_type='none',
                    students__payment_statuses__is_paid=True,
                    students__payment_statuses__invoice__in=invoice_qs,
                ) & ~Q(
                    students__payment_statuses__invoice__month=month,
                    students__payment_statuses__invoice__year=year,
                ),
                distinct=True,
            ),

            # Discount current month
            students_discount_current=Count(
                'students__payment_statuses',
                filter=Q(
                    students__discount_type='discount',
                    students__payment_statuses__is_paid=True,
                    students__payment_statuses__invoice__in=invoice_qs,
                    students__payment_statuses__invoice__month=month,
                    students__payment_statuses__invoice__year=year,
                ),
                distinct=True,
            ),

            # Discount previous months
            students_discount_previous=Count(
                'students__payment_statuses',
                filter=Q(
                    students__discount_type='discount',
                    students__payment_statuses__is_paid=True,
                    students__payment_statuses__invoice__in=invoice_qs,
                ) & ~Q(
                    students__payment_statuses__invoice__month=month,
                    students__payment_statuses__invoice__year=year,
                ),
                distinct=True,
            ),

            # Fully exempted students
            students_full_discount=Count(
                'students',
                filter=Q(students__discount_type='full'),
                distinct=True,
            ),
        )
        .annotate(
            # Unpaid current month
            students_not_paid=ExpressionWrapper(
                F('total_students') - (
                    F('students_paid_current') +
                    F('students_discount_current') +
                    F('students_full_discount')
                ),
                output_field=IntegerField(),
            ),

            # Total current month
            total_current_month=ExpressionWrapper(
                (F('students_paid_current') * F("price")) +
                (F('students_discount_current') * (F("price") - Value(discount_amount))),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),

            # Total previous months
            total_previous_months=ExpressionWrapper(
                (F('students_paid_previous') * F("price")) +
                (F('students_discount_previous') * (F("price") - Value(discount_amount))),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
        )
        .annotate(
            # Final total
            final_total=ExpressionWrapper(
                F('total_current_month') + F('total_previous_months'),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            )
        )
        .values(
            'name',
            'teacher__name',
            'start_time',
            'end_time',
            'total_students',

            'students_paid_current',
            'students_discount_current',
            'students_full_discount',
            'students_not_paid',

            'students_paid_previous',
            'students_discount_previous',

            'total_current_month',
            'total_previous_months',
            'final_total',
        )
    )

    return data

def get_payment_summary(school_id, from_date, to_date):
    filters = {
        'school_id': school_id
    }

    if from_date:
        filters['from_date'] = from_date
    if to_date:
        filters['to_date'] = to_date

    data = (
        StudentPaymentStatus.objects.filter(**filters)
        .annotate(
            date=F('invoice__date'),
            student_code=F('student__code'),
            student_name=F('student__name'),
            amount=F('invoice__amount'),
        )
        .values(
            'date',
            'student_code',
            'student_name',
            'month',
            'year',
            'amount',
        )
    )

    return data
