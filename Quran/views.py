import json
from datetime import date
from django.urls import reverse
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.contrib.admin.views.decorators import staff_member_required
from Quran.models import Student, Group, Attendance, Invoice, StudentPaymentStatus


def get_missing_months_for_student(student_id):
    start_year = 2025
    start_month = 1

    today = date.today()
    current_year = today.year
    current_month = today.month

    # Build list of all required (year, month) tuples from start to current
    required_months = []
    y, m = start_year, start_month
    while (y < current_year) or (y == current_year and m <= current_month):
        required_months.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1

    # Get all (year, month) pairs where the student has a payment status
    existing_months = StudentPaymentStatus.objects.filter(student_id=student_id).values_list('year', 'month')
    existing_months_set = set(existing_months)

    # Return months that are in required list but not in existing set
    missing_months = [
        f"{year}-{month:02d}"
        for (year, month) in required_months
        if (year, month) not in existing_months_set
    ]
    
    return missing_months


# Returns True or False if the student is marked present on the selected date.
def get_present_for_student(student_id, selected_date):
    attendance = Attendance.objects.filter(student_id=student_id, date=selected_date).first()
    present = attendance.present if attendance else False
    return present


@staff_member_required
def home(request):
    context = {}
    return render(request, 'home.html', context)


@staff_member_required
def attendance(request):
    groups = Group.objects.all()
    today = date.today()
    
    selected_date = request.GET.get('selected_date') or request.POST.get('selected_date')
    selected_group = request.GET.get('selected_group') or request.POST.get('selected_group')

    context = {
        'groups': groups,
        'today': today,
        'group_students': [],
        'selected_date': selected_date,
        'selected_group': selected_group,
    }

    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')
        
        for student_id in student_ids:
            key = f'present_{student_id}'
            present = key in request.POST
            
            Attendance.objects.update_or_create(
                date=selected_date,
                student_id=student_id,
                defaults={'present': present}
            )
        # Redirect back to the GET view with filters to see updated data
        return redirect(f"{reverse('attendance')}?selected_date={selected_date}&selected_group={selected_group}")


    # For GET requests, populate students only if both filters are set
    if selected_date and selected_group:
        students = Student.objects.filter(is_active=True, group=selected_group).values_list('id', 'code', 'name')
        for student_id, code, name in students:
            missing = get_missing_months_for_student(student_id)
            present = get_present_for_student(student_id, selected_date)
            context['group_students'].append({
                "student_id": student_id,
                "student_code": code,
                "student_name": name,
                "status": missing,
                "present": present,
            })

    return render(request, 'attendance.html', context)


@staff_member_required
def create_invoice(request):
    today = date.today()
    current_year = today.year
    current_month = today.month

    context = {
        "months": range(1, 13),
        "years": range(2025, 2031),
        "current_month": current_month,
        "current_year": current_year,
    }

    if request.method == 'GET':
        code = request.GET.get('selected_code')
        name = request.GET.get('selected_name')
        try:
            if code:
                student = Student.objects.get(code=code)
            elif name:
                student = Student.objects.get(name__icontains=name)
            else:
                student = None

            if student:
                context['student_data'] = {
                    'name': student.name,
                    'code': student.code,
                    'group': student.group,
                    'course': student.group.course.name if student else None,
                    'price': student.group.course.price if student else None,
                }
            else:
                context['error_msg'] = "Student Not Found."
        except Student.DoesNotExist:
            context['error_msg'] = "Student Not Found."
        return render(request, 'create_invoice.html', context)

    if request.method == 'POST':
        code = request.POST.get('student_code')
        year = request.POST.get('year')
        month = request.POST.get('month')
        amount = request.POST.get('amount')

        try:
            student = Student.objects.get(code=code)
            invoice = Invoice(
                student=student,
                month=month,
                year=year,
                amount=amount
            )
            invoice.save()
            return redirect('print_invoice', invoice_id=invoice.id)

        except ValidationError as error:
            context['student_data'] = {
                'name': student.name,
                'code': student.code,
                'group': student.group,
                'course': student.group.course.name if student else None,
                'price': student.group.course.price if student else None,
            }
            context['error_msg'] = ', '.join(error.message_dict.get('__all__', []))
            return render(request, 'create_invoice.html', context)

def print_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    return render(request, 'print_invoice.html', {'invoice': invoice})
