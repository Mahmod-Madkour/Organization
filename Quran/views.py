import json
from datetime import date
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView
)
from Quran.models import (
    Student, Teacher, Group, Attendance, Invoice, StudentPaymentStatus
)
from Quran.forms import (
    StudentForm, TeacherForm
)


# --------------------- Utilities ---------------------
def get_missing_months_for_student(student_id):
    start_year, start_month = 2025, 1
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


def get_present_for_student(student_id, selected_date):
    attendance = Attendance.objects.filter(student_id=student_id, date=selected_date).first()
    return attendance.present if attendance else False


# --------------------- Home ---------------------
@method_decorator(staff_member_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'Quran/home.html'


# --------------------- Attendance ---------------------
@method_decorator(staff_member_required, name='dispatch')
class AttendanceView(TemplateView):
    template_name = 'Quran/attendance/attendance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        selected_date = self.request.GET.get('selected_date') or self.request.POST.get('selected_date')
        selected_group = self.request.GET.get('selected_group') or self.request.POST.get('selected_group')

        context.update({
            'groups': Group.objects.all(),
            'today': today,
            'selected_date': selected_date,
            'selected_group': selected_group,
            'group_students': [],
        })

        if selected_date and selected_group:
            students = Student.objects.filter(is_active=True, group=selected_group)
            for student in students:
                missing = get_missing_months_for_student(student.id)
                present = get_present_for_student(student.id, selected_date)
                context['group_students'].append({
                    "student_id": student.id,
                    "student_code": student.code,
                    "student_name": student.name,
                    "status": missing,
                    "present": present,
                })
        return context

    def post(self, request, *args, **kwargs):
        selected_date = request.POST.get('selected_date')
        selected_group = request.POST.get('selected_group')
        student_ids = request.POST.getlist('student_ids')

        for student_id in student_ids:
            present = f'present_{student_id}' in request.POST
            Attendance.objects.update_or_create(
                date=selected_date,
                student_id=student_id,
                defaults={'present': present}
            )
        return redirect(f"{reverse('attendance')}?selected_date={selected_date}&selected_group={selected_group}")


# --------------------- Invoices ---------------------
@method_decorator(staff_member_required, name='dispatch')
class InvoiceCreateView(TemplateView):
    template_name = 'Quran/invoice/invoice.html'
    # success_url = reverse_lazy('invoice')

    def get_context_data(self, **kwargs):
        print("pass")
        context = super().get_context_data(**kwargs)
        print("pass", context)
        today = date.today()
        context.update({
            "months": range(1, 13),
            "years": range(2025, 2031),
            "current_month": today.month,
            "current_year": today.year,
        })
        code = self.request.GET.get('selected_code')
        name = self.request.GET.get('selected_name')

        student = None
        if code:
            student = Student.objects.filter(code=code).first()
        elif name:
            student = Student.objects.filter(name__icontains=name).first()

        if student:
            context['student_data'] = {
                'name': student.name,
                'code': student.code,
                'group': student.group,
                'course': student.group.course.name if student.group else None,
                'price': student.group.course.price if student.group else None,
            }
        elif (code or name):
            context['error_msg'] = "Student Not Found."

        return context

    def post(self, request, *args, **kwargs):
        code = request.POST.get('student_code')
        year = request.POST.get('year')
        month = request.POST.get('month')
        amount = request.POST.get('amount')

        try:
            student = Student.objects.get(code=code)
            invoice = Invoice.objects.create(
                student=student,
                month=month,
                year=year,
                amount=amount
            )
            return redirect('print_invoice', invoice_id=invoice.id)
        except ValidationError as error:
            context = self.get_context_data()
            context['error_msg'] = ', '.join(error.message_dict.get('__all__', []))
            return self.render_to_response(context)


@staff_member_required
def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'Quran/invoice/print_invoice.html', {'invoice': invoice})


# --------------------- Student ---------------------
@method_decorator(staff_member_required, name='dispatch')
class StudentListView(ListView):
    model = Student
    template_name = 'Quran/student/student_list.html'
    context_object_name = 'students'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(code__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


@method_decorator(staff_member_required, name='dispatch')
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'Quran/student/student_form.html'
    success_url = reverse_lazy('student_list')


@method_decorator(staff_member_required, name='dispatch')
class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'Quran/student/student_form.html'
    success_url = reverse_lazy('student_list')


@method_decorator(staff_member_required, name='dispatch')
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'Quran/student/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')


# --------------------- Teacher ---------------------
@method_decorator(staff_member_required, name='dispatch')
class TeacherListView(ListView):
    model = Teacher
    template_name = 'Quran/teacher/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(code__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

@method_decorator(staff_member_required, name='dispatch')
class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'Quran/teacher/teacher_form.html'
    success_url = reverse_lazy('teacher_list')


@method_decorator(staff_member_required, name='dispatch')
class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'Quran/teacher/teacher_form.html'
    success_url = reverse_lazy('teacher_list')


@method_decorator(staff_member_required, name='dispatch')
class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'Quran/teacher/teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher_list')
