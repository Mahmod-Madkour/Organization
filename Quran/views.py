import json
from datetime import date, timezone
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
    Student, Teacher, Course, ClassGroup, Attendance, Invoice, StudentPaymentStatus
)
from Quran.forms import (
    StudentForm, TeacherForm, CourseForm, ClassGroupForm
)
from Quran.utils import (
    get_user_school, get_present_for_student, get_missing_months_for_student
)
from Quran.services import (
    handle_academic_year
)


# --------------------- Home ---------------------
@method_decorator(staff_member_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'Quran/home.html'


# --------------------- Base Class ---------------------
class BaseListView(ListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        user_schools = get_user_school(self.request)
        if user_schools.exists():
            queryset = queryset.filter(school__in=user_schools)
        return queryset


class BaseCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'Quran/student/student_form.html'
    success_url = reverse_lazy('student_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.school = get_user_school(self.request).first()
        return super().form_valid(form)


class BaseUpdateView(UpdateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            form.instance.school = get_user_school(self.request).first()
        return super().form_valid(form)


# --------------------- Student ---------------------
@method_decorator(staff_member_required, name='dispatch')
class StudentListView(BaseListView):
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
class StudentCreateView(BaseCreateView):
    model = Student
    form_class = StudentForm
    template_name = 'Quran/student/student_form.html'
    success_url = reverse_lazy('student_list')


@method_decorator(staff_member_required, name='dispatch')
class StudentUpdateView(BaseUpdateView):
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
class TeacherListView(BaseListView):
    model = Teacher
    template_name = 'Quran/teacher/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(id_number__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

@method_decorator(staff_member_required, name='dispatch')
class TeacherCreateView(BaseCreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'Quran/teacher/teacher_form.html'
    success_url = reverse_lazy('teacher_list')


@method_decorator(staff_member_required, name='dispatch')
class TeacherUpdateView(BaseUpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'Quran/teacher/teacher_form.html'
    success_url = reverse_lazy('teacher_list')


@method_decorator(staff_member_required, name='dispatch')
class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'Quran/teacher/teacher_confirm_delete.html'
    success_url = reverse_lazy('teacher_list')


# --------------------- Course ---------------------
from django.contrib.auth.decorators import permission_required

@method_decorator(permission_required('Quran.view_course', raise_exception=True), name='dispatch')
class CourseListView(BaseListView):
    model = Course
    template_name = 'Quran/course/course_list.html'
    context_object_name = 'courses'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                name__icontains=search_query
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

@method_decorator(permission_required('Quran.add_course', raise_exception=True), name='dispatch')
class CourseCreateView(BaseCreateView):
    model = Course
    form_class = CourseForm
    template_name = 'Quran/course/course_form.html'
    success_url = reverse_lazy('course_list')


@method_decorator(permission_required('Quran.change_course', raise_exception=True), name='dispatch')
class CourseUpdateView(BaseUpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'Quran/course/course_form.html'
    success_url = reverse_lazy('course_list')


@method_decorator(permission_required('Quran.delete_course', raise_exception=True), name='dispatch')
class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'Quran/course/course_confirm_delete.html'
    success_url = reverse_lazy('course_list')


# --------------------- ClassGroup ---------------------
@method_decorator(staff_member_required, name='dispatch')
class ClassGroupListView(BaseListView):
    model = ClassGroup
    template_name = 'Quran/class_group/class_group_list.html'
    context_object_name = 'class_groups'
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
class ClassGroupCreateView(BaseCreateView):
    model = ClassGroup
    form_class = ClassGroupForm
    template_name = 'Quran/class_group/class_group_form.html'
    success_url = reverse_lazy('class_group_list')


@method_decorator(staff_member_required, name='dispatch')
class ClassGroupUpdateView(BaseUpdateView):
    model = ClassGroup
    form_class = ClassGroupForm
    template_name = 'Quran/class_group/class_group_form.html'
    success_url = reverse_lazy('class_group_list')


@method_decorator(staff_member_required, name='dispatch')
class ClassGroupDeleteView(DeleteView):
    model = ClassGroup
    template_name = 'Quran/class_group/class_group_confirm_delete.html'
    success_url = reverse_lazy('class_group_list')



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
            'groups': ClassGroup.objects.all(),
            'today': today,
            'selected_date': selected_date,
            'selected_group': selected_group,
            'group_students': [],
        })

        if selected_date and selected_group:
            students = Student.objects.filter(is_active=True, group=selected_group)
            for student in students:
                missing = get_missing_months_for_student(student)
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
        present_student_ids = request.POST.getlist('present')

        for student_id in student_ids:
            present = str(student_id) in present_student_ids
            student = Student.objects.get(id=student_id)

            Attendance.objects.update_or_create(
                school=student.school,
                student=student,
                date=selected_date,
                defaults={'present': present}
            )

        # After saving, just render the updated context
        context = self.get_context_data()
        context['selected_date'] = selected_date
        context['selected_group'] = selected_group

        return self.render_to_response(context)


# --------------------- Invoices ---------------------
@method_decorator(staff_member_required, name='dispatch')
class InvoiceCreateView(TemplateView):
    template_name = 'Quran/invoice/invoice.html'

    def get_student(self, code=None, name=None):
        """Return the student object based on code or name."""
        if code:
            return Student.objects.filter(code=code).first()
        if name:
            return Student.objects.filter(name__icontains=name).first()
        return None

    def build_student_context(self, student):
        """Return context dictionary for a student."""
        expected_price = Invoice.calculate_expected_amount(student)
        return {
            "id": student.id,
            "code": student.code,
            "name": student.name,
            "group": student.group.name,
            "course": student.group.course.name,
            "price": expected_price,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        current_month = today.month
        current_year = today.year
        context.update({
            "months": range(1, 13),
            "years": range(current_year, current_year + 10),
            "current_month": current_month,
            "current_year": current_year,
        })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        selected_code = request.GET.get("selected_code")
        selected_name = request.GET.get("selected_name")

        context.update({
            "selected_code": selected_code,
            "selected_name": selected_name,
        })

        student = self.get_student(code=selected_code, name=selected_name)
        if not student:
            context["error_msg"] = "Student not found."
            return render(request, self.template_name, context)

        if student.discount_type == 'full':
            context["error_msg"] = "Student is exempt."
            return render(request, self.template_name, context)

        context["student_data"] = self.build_student_context(student)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        code = request.POST.get('student_code')
        year = request.POST.get('year')
        month = request.POST.get('month')

        student = self.get_student(code=code)
        if not student:
            context["error_msg"] = "Student not found."
            return render(request, self.template_name, context)

        if student.discount_type == 'full':
            context["error_msg"] = "Student is exempt."
            return render(request, self.template_name, context)

        context["student_data"] = self.build_student_context(student)

        # Check duplicate invoice
        if Invoice.objects.filter(student=student, month=month, year=year).exists():
            context["error_msg"] = f"An invoice already exists for {month}/{year}."
            return self.render_to_response(context)

        # Create invoice safely
        invoice = Invoice(
            school=student.school,
            student=student,
            month=month,
            year=year,
            amount=Invoice.calculate_expected_amount(student),
        )
        
        try:
            invoice.save()
            return redirect("print_invoice", invoice_id=invoice.id)
        except ValidationError as e:
            context["error_msg"] = "; ".join(e.messages)
            return self.render_to_response(context)


@staff_member_required
def print_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    return render(request, 'Quran/invoice/print_invoice.html', {'invoice': invoice})


if __name__ == "__main__":
    # upgrade academic year
    today = timezone.now().date()
    if today.month == 9 and today.day == 1:
        handle_academic_year()
