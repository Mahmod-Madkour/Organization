# Quran Organization Management System

A comprehensive Django-based management system for Quranic education organizations, featuring student management, teacher administration, course scheduling, attendance tracking, and financial management.

## 🌟 Features

### Core Management
- **Student Management**: Complete student lifecycle management with personal information, academic details, and enrollment tracking
- **Teacher Management**: Teacher profiles, qualifications, and class assignments
- **Course Management**: Quranic course creation, scheduling, and curriculum management
- **Class Group Management**: Organize students into classes and manage group dynamics

### Attendance & Tracking
- **Daily Attendance**: Track student attendance with detailed records
- **Monthly Attendance Reports**: Comprehensive monthly attendance summaries with statistics
- **Attendance Analytics**: Visual reports and attendance patterns

### Financial Management
- **Invoice Generation**: Create and manage student invoices with automatic calculations
- **Payment Tracking**: Monitor payment status and financial records
- **PDF Invoice Printing**: Professional invoice generation with printable PDFs

### Internationalization
- **Multi-language Support**: English and Arabic language support
- **RTL Support**: Right-to-left language support for Arabic
- **Localized Interface**: Full translation of UI elements and content

### Additional Features
- **Responsive Design**: Mobile-friendly interface using modern CSS frameworks
- **Search & Filtering**: Advanced search capabilities for all data
- **Data Export**: Export data to Excel formats
- **User Authentication**: Secure login system with role-based access
- **Admin Panel**: Comprehensive Django admin integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 5.0+
- SQLite (included)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Organization
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load initial data** (optional)
   ```bash
   python auto_fill_data.py
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
Organization/
├── Organization/                 # Django project settings
│   ├── settings.py              # Project configuration
│   ├── urls.py                  # Main URL routing
│   └── wsgi.py                  # WSGI configuration
├── Quran/                       # Main application
│   ├── models.py                # Database models
│   ├── views.py                 # View logic
│   ├── forms.py                 # Form definitions
│   ├── urls.py                  # App URL routing
│   ├── admin.py                 # Admin interface
│   ├── templates/               # HTML templates
│   ├── static/                  # Static files (CSS, JS, images)
│   └── utils.py                 # Utility functions
├── templates/                   # Global templates
├── static/                      # Global static files
├── locale/                      # Translation files
│   └── ar/                      # Arabic translations
├── Data/                        # Data files
├── auto_fill_data.py           # Initial data population
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🎯 Main Modules

### Student Management
- Personal information tracking (name, ID, contact details)
- Academic year and level management
- Gender and marital status tracking
- Photo upload support

### Teacher Management
- Professional information and qualifications
- Contact details and availability
- Course assignment capabilities

### Course Management
- Course creation and scheduling
- Pricing and duration management
- Teacher assignment

### Attendance System
- Daily attendance recording
- Monthly attendance summaries
- Attendance statistics and reports
- Export to Excel functionality

### Financial Management
- Invoice generation with automatic calculations
- Payment status tracking
- PDF invoice printing
- Financial reporting

## 🔧 Configuration

### Environment Variables
The project uses Django's built-in settings. Key configurations in `Organization/settings.py`:

- `SECRET_KEY`: Django secret key (change in production)
- `DEBUG`: Debug mode (set to False in production)
- `ALLOWED_HOSTS`: Allowed hosts for deployment
- `DATABASE`: SQLite database configuration

### Internationalization
- Supported languages: English, Arabic
- Translation files located in `locale/`
- RTL support for Arabic interface

## 🌐 Deployment

### Production Deployment

1. **Set production settings**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Database migrations**
   ```bash
   python manage.py migrate
   ```

4. **WSGI deployment**
   - Use Gunicorn or uWSGI
   - Configure Nginx as reverse proxy
   - Set up SSL certificates

### PythonAnywhere Deployment
The project is configured for PythonAnywhere deployment with the allowed host `mmadkour.pythonanywhere.com`.

## 📊 Database Schema

### Core Models
- **Student**: Student information and enrollment details
- **Teacher**: Teacher profiles and qualifications
- **Course**: Course information and scheduling
- **ClassGroup**: Class organization and student assignments
- **Attendance**: Attendance records and tracking
- **Invoice**: Financial invoicing and payment tracking

## 🛠️ Dependencies

- **Django 5.0.4**: Web framework
- **django-select2 8.1.0**: Enhanced select widgets
- **Pillow 10.1.0**: Image processing
- **python-decouple 3.8**: Configuration management
- **pandas 2.1.4**: Data manipulation and export
- **openpyxl 3.1.2**: Excel file handling

## 📝 API Documentation

The application follows Django's class-based views pattern:

### Main Views
- `HomeView`: Dashboard and overview
- `Student*Views`: CRUD operations for students
- `Teacher*Views`: CRUD operations for teachers
- `Course*Views`: CRUD operations for courses
- `AttendanceView`: Daily attendance management
- `MonthlyAttendanceView`: Monthly attendance reports
- `InvoiceCreateView`: Invoice generation
- `PaymentStatusListView`: Payment tracking

## 🔒 Security

- Django's built-in authentication system
- CSRF protection enabled
- SQL injection prevention through Django ORM
- Secure password handling
- Session management

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📈 Performance

- SQLite database for efficient storage
- Optimized queries through Django ORM
- Static file compression
- Efficient template rendering

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Review the documentation
- Check Django's official documentation

## 📄 License

This project is licensed under the MIT License.

---

**Note**: This is a Django-based educational management system specifically designed for Quranic education organizations. The system provides comprehensive tools for managing students, teachers, courses, attendance, and financial operations with multilingual support.
