# Development Guide

## Overview

This guide covers development practices, coding standards, and contribution guidelines for the Quran Organization Management System.

## Development Environment Setup

### Prerequisites
- Python 3.8+
- Git
- Code editor (VS Code recommended)
- Virtual environment tool

### Quick Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd Organization
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements_dev.txt  # If exists
   ```

4. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python auto_fill_data.py  # Load sample data
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

### Application Structure
```
Organization/
├── Organization/                 # Django project
│   ├── __init__.py
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Main URLs
│   ├── wsgi.py                  # WSGI config
│   └── asgi.py                  # ASGI config
├── Quran/                       # Main app
│   ├── __init__.py
│   ├── admin.py                 # Admin interface
│   ├── apps.py                  # App config
│   ├── forms.py                 # Form classes
│   ├── models.py                # Database models
│   ├── signals.py               # Signal handlers
│   ├── urls.py                  # App URLs
│   ├── utils.py                 # Utility functions
│   ├── views.py                 # View logic
│   ├── management/              # Management commands
│   ├── migrations/              # Database migrations
│   ├── templates/               # App templates
│   └── static/                  # App static files
├── templates/                   # Global templates
├── static/                      # Global static files
├── locale/                      # Translations
├── docs/                        # Documentation
└── tests/                       # Test files
```

### Code Organization

**Models** (`Quran/models.py`)
- All database models
- Model methods and properties
- Model validation
- Custom managers (if any)

**Views** (`Quran/views.py`)
- Class-based views preferred
- View logic and business rules
- Response handling
- Permission checks

**Forms** (`Quran/forms.py`)
- Django forms
- Form validation
- Custom form fields
- Form widgets

**Templates** (`Quran/templates/`)
- HTML templates
- Template inheritance
- Static file inclusion
- Translation tags

**Utils** (`Quran/utils.py`)
- Helper functions
- Business logic
- Data processing
- Export functions

## Coding Standards

### Python Code Style

**Follow PEP 8**
- Maximum line length: 79 characters
- Use 4 spaces for indentation
- Use snake_case for variables and functions
- Use PascalCase for classes

**Import Organization**
```python
# Standard library imports
import os
from datetime import datetime

# Third-party imports
from django.db import models
from django.contrib.auth.models import User

# Local imports
from .utils import helper_function
```

**Docstrings**
```python
def calculate_attendance_rate(student, month, year):
    """
    Calculate attendance rate for a student in a specific month.
    
    Args:
        student (Student): Student instance
        month (int): Month number (1-12)
        year (int): Year
        
    Returns:
        float: Attendance percentage (0-100)
        
    Raises:
        ValueError: If month or year is invalid
    """
    pass
```

### Django Best Practices

**Model Design**
```python
class Student(models.Model):
    """Model for managing student information."""
    
    name = models.CharField(
        max_length=100,
        verbose_name=_("Full Name"),
        help_text=_("Enter student's full name")
    )
    
    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})
```

**View Classes**
```python
class StudentListView(LoginRequiredMixin, ListView):
    """List view for students with search and filtering."""
    
    model = Student
    template_name = 'quran/student_list.html'
    context_object_name = 'students'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) |
                models.Q(national_id__icontains=search)
            )
        return queryset
```

**Form Classes**
```python
class StudentForm(forms.ModelForm):
    """Form for creating and updating students."""
    
    class Meta:
        model = Student
        fields = ['name', 'national_id', 'phone', 'gender']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Enter full name')
            })
        }
    
    def clean_national_id(self):
        """Validate national ID format."""
        national_id = self.cleaned_data['national_id']
        if not re.match(r'^\d{14}$', national_id):
            raise forms.ValidationError(_("ID must be exactly 14 digits"))
        return national_id
```

## Development Workflow

### Git Workflow

**Branch Naming**
- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/urgent-fix` - Critical fixes
- `docs/documentation` - Documentation updates

**Commit Messages**
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(students): add bulk import functionality
fix(attendance): resolve date validation error
docs(readme): update installation instructions
```

**Development Process**
1. Create feature branch
2. Make changes with small, focused commits
3. Test thoroughly
4. Create pull request
5. Code review
6. Merge to main branch

### Testing

**Running Tests**
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test Quran

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

**Writing Tests**
```python
from django.test import TestCase, Client
from django.urls import reverse
from Quran.models import Student

class StudentModelTest(TestCase):
    """Test cases for Student model."""
    
    def setUp(self):
        self.student = Student.objects.create(
            name="Test Student",
            national_id="12345678901234",
            phone="01234567890"
        )
    
    def test_student_creation(self):
        """Test student model creation."""
        self.assertEqual(self.student.name, "Test Student")
        self.assertEqual(str(self.student), "Test Student")
    
    def test_student_age_calculation(self):
        """Test age calculation method."""
        # Add age calculation test
        pass

class StudentViewTest(TestCase):
    """Test cases for student views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_student_list_view(self):
        """Test student list view."""
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Students')
```

### Debugging

**Django Debug Toolbar**
```python
# Add to INSTALLED_APPS in settings.py
'debug_toolbar',

# Add to MIDDLEWARE
'debug_toolbar.middleware.DebugToolbarMiddleware',

# Add to URLs
if DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
```

**Logging Configuration**
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'Quran': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

**Database Debugging**
```python
# Enable query logging
from django.db import connection

def some_view(request):
    # Your code here
    print(connection.queries)  # Show all queries
```

## Frontend Development

### CSS Organization

**File Structure**
```
static/
├── css/
│   ├── base.css           # Base styles
│   ├── components.css     # Component styles
│   ├── layout.css         # Layout styles
│   └── responsive.css     # Responsive styles
├── js/
│   ├── main.js           # Main JavaScript
│   ├── forms.js          # Form handling
│   └── charts.js         # Chart functionality
└── images/
    ├── icons/
    └── backgrounds/
```

**CSS Guidelines**
- Use BEM methodology for class naming
- Mobile-first responsive design
- CSS variables for theming
- Minimize use of !important

### JavaScript Development

**Best Practices**
- Use modern ES6+ features
- Separate concerns (DOM manipulation, business logic)
- Handle errors gracefully
- Use event delegation for dynamic content

**Example**
```javascript
// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form[data-validate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
});

function validateForm(form) {
    // Validation logic
    return true;
}
```

## Database Development

### Migrations

**Creating Migrations**
```bash
# Create migration for model changes
python manage.py makemigrations

# Create migration for specific app
python manage.py makemigrations Quran

# Create empty migration
python manage.py makemigrations --empty Quran
```

**Running Migrations**
```bash
# Apply all migrations
python manage.py migrate

# Apply specific migration
python manage.py migrate Quran 0001

# Show migration status
python manage.py showmigrations
```

**Data Migrations**
```python
# Quran/migrations/0002_populate_data.py
from django.db import migrations

def populate_academic_years(apps, schema_editor):
    Student = apps.get_model('Quran', 'Student')
    # Data migration logic
    pass

def reverse_populate_academic_years(apps, schema_editor):
    # Reverse migration logic
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('Quran', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            populate_academic_years,
            reverse_populate_academic_years,
        ),
    ]
```

### Query Optimization

**Select Related**
```python
# Use for foreign key relationships
students = Student.objects.select_related('teacher').all()
```

**Prefetch Related**
```python
# Use for many-to-many relationships
courses = Course.objects.prefetch_related('students').all()
```

**Query Optimization**
```python
# Avoid N+1 queries
students = Student.objects.prefetch_related(
    'attendance_set__class_group'
).all()
```

## Internationalization

### Translation Setup

**Settings Configuration**
```python
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('ar', _('Arabic')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
```

**Creating Translation Files**
```bash
# Create translation files
python manage.py makemessages -l ar

# Update translation files
python manage.py makemessages -l ar --update

# Compile translations
python manage.py compilemessages
```

**Using Translations**
```python
# In Python code
from django.utils.translation import gettext_lazy as _

name = models.CharField(
    max_length=100,
    verbose_name=_("Full Name")
)

# In templates
{% load i18n %}
<h1>{% trans "Student Management" %}</h1>
```

## Performance Optimization

### Database Performance

**Indexing**
```python
class Student(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    national_id = models.CharField(max_length=14, unique=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['name', 'academic_year']),
        ]
```

**Query Optimization**
```python
# Efficient queries
students = Student.objects.filter(
    academic_year='primary_1'
).select_related('teacher').only('name', 'national_id')
```

### Caching

**View Caching**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 minutes
def student_list_view(request):
    # View logic
    pass
```

**Template Caching**
```html
{% load cache %}
{% cache 500 student_sidebar %}
    <!-- Sidebar content -->
{% endcache %}
```

## Security Best Practices

### Input Validation

**Form Validation**
```python
class StudentForm(forms.ModelForm):
    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if not re.match(r'^\d{14}$', national_id):
            raise forms.ValidationError("Invalid ID format")
        return national_id
```

**SQL Injection Prevention**
```python
# Use Django ORM (safe)
students = Student.objects.filter(name__icontains=search)

# Avoid raw SQL (dangerous)
# cursor.execute(f"SELECT * FROM student WHERE name LIKE '%{search}%'")
```

### Authentication

**Permission Checks**
```python
from django.contrib.auth.mixins import LoginRequiredMixin

class StudentCreateView(LoginRequiredMixin, CreateView):
    # View requires authentication
    pass
```

**CSRF Protection**
```python
# All POST forms automatically include CSRF token
<form method="post">
    {% csrf_token %}
    <!-- Form fields -->
</form>
```

## Tools and Utilities

### Development Tools

**Code Quality**
```bash
# Install development tools
pip install flake8 black isort

# Format code
black .

# Sort imports
isort .

# Check code quality
flake8 .
```

**Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 22.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.10.1
    hooks:
      - id: isort
```

### Useful Django Packages

**Development**
- `django-debug-toolbar`: Debug information panel
- `django-extensions`: Additional management commands
- `factory-boy`: Test data generation

**Production**
- `django-cors-headers`: CORS handling
- `django-storages`: File storage backends
- `celery`: Background tasks

## Contributing Guidelines

### Code Review Process

1. **Self-Review**
   - Code follows style guidelines
   - Tests are included
   - Documentation is updated

2. **Peer Review**
   - Logic correctness
   - Security implications
   - Performance considerations

3. **Integration Testing**
   - Run full test suite
   - Manual testing of new features
   - Performance testing if needed

### Documentation

**Code Documentation**
- Docstrings for all functions and classes
- Inline comments for complex logic
- Type hints where appropriate

**User Documentation**
- Update README for new features
- Update API documentation
- Add user guide sections

## Troubleshooting

### Common Development Issues

**Migration Conflicts**
```bash
# Resolve migration conflicts
python manage.py migrate --merge
```

**Static File Issues**
```bash
# Clear static files
python manage.py collectstatic --clear --noinput
```

**Template Not Found**
```bash
# Check template directories
python manage.py findtemplate template_name.html
```

### Performance Issues

**Slow Queries**
- Use Django Debug Toolbar
- Check query count
- Add database indexes

**Memory Issues**
- Profile memory usage
- Optimize querysets
- Use pagination

## Resources

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

### Tools
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/)
- [Django Extensions](https://django-extensions.readthedocs.io/)
- [Factory Boy](https://factoryboy.readthedocs.io/)

### Communities
- [Django Users Mailing List](https://groups.google.com/group/django-users)
- [Reddit r/django](https://www.reddit.com/r/django/)
- [Stack Overflow Django Tag](https://stackoverflow.com/questions/tagged/django)
