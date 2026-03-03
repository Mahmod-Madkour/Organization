# API Documentation

## Overview

The Quran Organization Management System follows Django's class-based views pattern with RESTful-like URL structure. The application uses Django's built-in authentication and authorization.

## Base URL
```
http://127.0.0.1:8000/
```

## Authentication

All views require authentication except the login page. The system uses Django's session-based authentication.

### Authentication Endpoints
- `GET /login/` - Login page
- `POST /login/` - Login submission
- `POST /logout/` - Logout

## API Endpoints

### Dashboard
#### Home View
- **URL**: `GET /`
- **View**: `HomeView`
- **Description**: Main dashboard with system overview
- **Authentication**: Required
- **Response**: Dashboard HTML with statistics and recent activities

### Student Management

#### Student List
- **URL**: `GET /students/`
- **View**: `StudentListView`
- **Description**: Lists all students with search and filtering
- **Authentication**: Required
- **Query Parameters**:
  - `search`: Search by name, ID, or phone
  - `gender`: Filter by gender
  - `academic_year`: Filter by academic year
- **Response**: Paginated student list HTML

#### Create Student
- **URL**: `GET /students/add/`
- **View**: `StudentCreateView`
- **Description**: Display student creation form
- **Authentication**: Required
- **Response**: Student creation form HTML

- **URL**: `POST /students/add/`
- **Description**: Submit new student data
- **Request**: Student form data
- **Response**: Redirect to student list on success

#### Update Student
- **URL**: `GET /students/<int:pk>/edit/`
- **View**: `StudentUpdateView`
- **Description**: Display student edit form
- **Parameters**: `pk` - Student ID
- **Authentication**: Required
- **Response**: Student edit form HTML

- **URL**: `POST /students/<int:pk>/edit/`
- **Description**: Update student data
- **Request**: Updated student form data
- **Response**: Redirect to student list on success

#### Delete Student
- **URL**: `POST /students/<int:pk>/delete/`
- **View**: `StudentDeleteView`
- **Description**: Delete student record
- **Parameters**: `pk` - Student ID
- **Authentication**: Required
- **Response**: Redirect to student list

### Teacher Management

#### Teacher List
- **URL**: `GET /teachers/`
- **View**: `TeacherListView`
- **Description**: Lists all teachers with search and filtering
- **Authentication**: Required
- **Query Parameters**:
  - `search`: Search by name, ID, or phone
  - `specialization`: Filter by specialization
- **Response**: Paginated teacher list HTML

#### Create Teacher
- **URL**: `GET /teachers/add/`
- **View**: `TeacherCreateView`
- **Description**: Display teacher creation form
- **Authentication**: Required
- **Response**: Teacher creation form HTML

- **URL**: `POST /teachers/add/`
- **Description**: Submit new teacher data
- **Request**: Teacher form data
- **Response**: Redirect to teacher list on success

#### Update Teacher
- **URL**: `GET /teachers/<int:pk>/edit/`
- **View**: `TeacherUpdateView`
- **Description**: Display teacher edit form
- **Parameters**: `pk` - Teacher ID
- **Authentication**: Required
- **Response**: Teacher edit form HTML

- **URL**: `POST /teachers/<int:pk>/edit/`
- **Description**: Update teacher data
- **Request**: Updated teacher form data
- **Response**: Redirect to teacher list on success

#### Delete Teacher
- **URL**: `POST /teachers/<int:pk>/delete/`
- **View**: `TeacherDeleteView`
- **Description**: Delete teacher record
- **Parameters**: `pk` - Teacher ID
- **Authentication**: Required
- **Response**: Redirect to teacher list

### Course Management

#### Course List
- **URL**: `GET /courses/`
- **View**: `CourseListView`
- **Description**: Lists all courses with filtering
- **Authentication**: Required
- **Query Parameters**:
  - `search`: Search by name
  - `teacher`: Filter by teacher
  - `is_active`: Filter by active status
- **Response**: Paginated course list HTML

#### Create Course
- **URL**: `GET /courses/add/`
- **View**: `CourseCreateView`
- **Description**: Display course creation form
- **Authentication**: Required
- **Response**: Course creation form HTML

- **URL**: `POST /courses/add/`
- **Description**: Submit new course data
- **Request**: Course form data
- **Response**: Redirect to course list on success

#### Update Course
- **URL**: `GET /courses/<int:pk>/edit/`
- **View**: `CourseUpdateView`
- **Description**: Display course edit form
- **Parameters**: `pk` - Course ID
- **Authentication**: Required
- **Response**: Course edit form HTML

- **URL**: `POST /courses/<int:pk>/edit/`
- **Description**: Update course data
- **Request**: Updated course form data
- **Response**: Redirect to course list on success

#### Delete Course
- **URL**: `POST /courses/<int:pk>/delete/`
- **View**: `CourseDeleteView`
- **Description**: Delete course record
- **Parameters**: `pk` - Course ID
- **Authentication**: Required
- **Response**: Redirect to course list

### Class Group Management

#### Class Group List
- **URL**: `GET /class_groups/`
- **View**: `ClassGroupListView`
- **Description**: Lists all class groups
- **Authentication**: Required
- **Query Parameters**:
  - `course`: Filter by course
  - `teacher`: Filter by teacher
- **Response**: Paginated class group list HTML

#### Create Class Group
- **URL**: `GET /class_groups/add/`
- **View**: `ClassGroupCreateView`
- **Description**: Display class group creation form
- **Authentication**: Required
- **Response**: Class group creation form HTML

- **URL**: `POST /class_groups/add/`
- **Description**: Submit new class group data
- **Request**: Class group form data
- **Response**: Redirect to class group list on success

#### Update Class Group
- **URL**: `GET /class_groups/<int:pk>/edit/`
- **View**: `ClassGroupUpdateView`
- **Description**: Display class group edit form
- **Parameters**: `pk` - Class Group ID
- **Authentication**: Required
- **Response**: Class group edit form HTML

- **URL**: `POST /class_groups/<int:pk>/edit/`
- **Description**: Update class group data
- **Request**: Updated class group form data
- **Response**: Redirect to class group list on success

#### Delete Class Group
- **URL**: `POST /class_groups/<int:pk>/delete/`
- **View**: `ClassGroupDeleteView`
- **Description**: Delete class group record
- **Parameters**: `pk` - Class Group ID
- **Authentication**: Required
- **Response**: Redirect to class group list

### Attendance Management

#### Daily Attendance
- **URL**: `GET /attendance/`
- **View**: `AttendanceView`
- **Description**: Daily attendance recording interface
- **Authentication**: Required
- **Query Parameters**:
  - `date`: Specific date (defaults to today)
  - `class_group`: Filter by class group
- **Response**: Attendance recording form HTML

- **URL**: `POST /attendance/`
- **Description**: Submit attendance data
- **Request**: Attendance data for multiple students
- **Response**: Redirect to attendance page with success message

#### Monthly Attendance
- **URL**: `GET /monthly_attendance/`
- **View**: `MonthlyAttendanceView`
- **Description**: Monthly attendance reports
- **Authentication**: Required
- **Query Parameters**:
  - `month`: Month number (1-12)
  - `year`: Year
  - `student`: Filter by student
  - `class_group`: Filter by class group
- **Response**: Monthly attendance report HTML

### Invoice Management

#### Create Invoice
- **URL**: `GET /invoice/`
- **View**: `InvoiceCreateView`
- **Description**: Invoice creation form
- **Authentication**: Required
- **Response**: Invoice creation form HTML

- **URL**: `POST /invoice/`
- **Description**: Submit new invoice
- **Request**: Invoice form data
- **Response**: Redirect to payment status page

#### Print Invoice
- **URL**: `GET /invoice/print/<int:invoice_id>/`
- **View**: `InvoicePrintView`
- **Description**: Generate printable PDF invoice
- **Parameters**: `invoice_id` - Invoice ID
- **Authentication**: Required
- **Response**: PDF invoice download

### Payment Status

#### Payment List
- **URL**: `GET /payment_status/`
- **View**: `PaymentStatusListView`
- **Description**: List all invoices with payment status
- **Authentication**: Required
- **Query Parameters**:
  - `status`: Filter by payment status (Paid/Unpaid/Partial)
  - `student`: Filter by student
  - `date_range`: Filter by date range
- **Response**: Payment status list HTML

### Reports

#### Summary Report
- **URL**: `GET /summary/`
- **View**: `SummaryReportView`
- **Description**: System summary reports
- **Authentication**: Required
- **Query Parameters**:
  - `report_type`: Type of summary report
  - `date_range`: Date range for report
- **Response**: Summary report HTML

## Response Formats

### HTML Responses
Most endpoints return HTML responses for web interface consumption.

### PDF Responses
- Invoice printing returns PDF content-type
- Downloadable files with proper headers

### Error Responses
- **400 Bad Request**: Invalid form data
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Server Error**: Internal server error

## Status Codes

- **200 OK**: Successful GET request
- **302 Found**: Redirect after successful POST
- **400 Bad Request**: Validation errors
- **403 Forbidden**: Authentication required
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## Pagination

List views support pagination with:
- Default page size: 20 items
- Page parameter: `?page=2`
- Next/Previous navigation

## Search and Filtering

### Common Search Parameters
- `search`: Text search across multiple fields
- `status`: Filter by status
- `date`: Date filtering
- `date_range`: Date range filtering

### Filtering Options
- Gender filtering for students/teachers
- Academic year filtering for students
- Course/Teacher filtering for classes
- Payment status filtering for invoices

## Data Export

### Excel Export
- Monthly attendance reports can be exported to Excel
- Payment status reports support Excel export
- Student lists support Excel export

### Export Endpoints
- Export functionality integrated into list views
- Download links generated dynamically
- File names include timestamp

## Security

### CSRF Protection
All POST requests require CSRF tokens.

### Authentication Required
All endpoints except login require authenticated user.

### Authorization
User must have appropriate permissions for each action.

## Error Handling

### Form Validation
- Server-side validation
- Client-side validation hints
- User-friendly error messages

### Database Errors
- Constraint violation handling
- Transaction rollback on errors
- User-friendly error pages

## Performance

### Query Optimization
- Select related objects where possible
- Prefetch related objects for lists
- Database indexes on foreign keys

### Caching
- Static file caching
- Template fragment caching (if implemented)

## Internationalization

### Language Support
- URLs support language switching
- Content translated based on user preference
- Date/time formatting localized

### RTL Support
- Arabic language uses RTL layout
- CSS automatically adjusts for text direction
