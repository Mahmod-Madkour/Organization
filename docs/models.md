# Database Models Documentation

## Overview

The Quran Organization Management System uses Django ORM with SQLite database. The models are designed to manage students, teachers, courses, attendance, and financial operations.

## Core Models

### Student Model

**Purpose**: Manages student information and enrollment details.

**Fields**:
- `name` (CharField): Student full name
- `national_id` (CharField): 14-digit national ID number
- `phone` (CharField): 11-digit phone number
- `gender` (CharField): Gender choice (Male/Female)
- `marital_status` (CharField): Marital status (Single/Married/Divorced/Widowed)
- `academic_year` (CharField): Academic year level (Pre-Primary to Graduate)
- `birth_date` (DateField): Date of birth
- `address` (TextField): Residential address
- `photo` (ImageField): Student photo (optional)
- `enrollment_date` (DateField): Date of enrollment
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Validation**:
- National ID: Exactly 14 digits
- Phone number: Exactly 11 digits
- Required fields: name, national_id, phone

### Teacher Model

**Purpose**: Manages teacher profiles and professional information.

**Fields**:
- `name` (CharField): Teacher full name
- `national_id` (CharField): 14-digit national ID number
- `phone` (CharField): 11-digit phone number
- `gender` (CharField): Gender choice (Male/Female)
- `marital_status` (CharField): Marital status
- `academic_qualification` (CharField): Highest academic qualification
- `specialization` (CharField): Teaching specialization
- `experience_years` (PositiveIntegerField): Years of teaching experience
- `hire_date` (DateField): Date of hiring
- `salary` (DecimalField): Monthly salary
- `address` (TextField): Residential address
- `photo` (ImageField): Teacher photo (optional)
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Validation**:
- National ID: Exactly 14 digits
- Phone number: Exactly 11 digits
- Experience years: Positive integer
- Required fields: name, national_id, phone, academic_qualification

### Course Model

**Purpose**: Manages Quranic courses and scheduling.

**Fields**:
- `name` (CharField): Course name
- `description` (TextField): Course description
- `teacher` (ForeignKey): Assigned teacher
- `duration_weeks` (PositiveIntegerField): Course duration in weeks
- `price` (DecimalField): Course fee
- `start_date` (DateField): Course start date
- `end_date` (DateField): Course end date
- `max_students` (PositiveIntegerField): Maximum student capacity
- `is_active` (BooleanField): Course active status
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Validation**:
- End date must be after start date
- Price must be positive
- Max students must be positive

### ClassGroup Model

**Purpose**: Organizes students into classes and groups.

**Fields**:
- `name` (CharField): Class/group name
- `course` (ForeignKey): Associated course
- `teacher` (ForeignKey): Assigned teacher
- `students` (ManyToManyField): Enrolled students
- `schedule` (CharField): Class schedule (e.g., "Saturday 9:00 AM")
- `max_capacity` (PositiveIntegerField): Maximum students
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Validation**:
- Course and teacher must be active
- Max capacity must be positive

### Attendance Model

**Purpose**: Tracks student attendance records.

**Fields**:
- `student` (ForeignKey): Attending student
- `class_group` (ForeignKey): Class group
- `date` (DateField): Attendance date
- `status` (CharField): Attendance status (Present/Absent/Late)
- `notes` (TextField): Additional notes (optional)
- `recorded_by` (ForeignKey): User who recorded attendance
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Validation**:
- Unique constraint on student, class_group, and date
- Status must be valid choice

### Invoice Model

**Purpose**: Manages financial invoicing for students.

**Fields**:
- `student` (ForeignKey): Billing student
- `course` (ForeignKey): Associated course
- `amount` (DecimalField): Invoice amount
- `due_date` (DateField): Payment due date
- `status` (CharField): Payment status (Paid/Unpaid/Partial)
- `paid_amount` (DecimalField): Amount paid
- `issue_date` (DateField): Invoice issue date
- `notes` (TextField): Additional notes
- `created_by` (ForeignKey): User who created invoice
- `created_at` (DateTimeField): Record creation timestamp
- `updated_at` (DateTimeField): Last update timestamp

**Validation**:
- Amount must be positive
- Paid amount cannot exceed total amount
- Due date must be after issue date

## Relationships

### Many-to-Many Relationships
- **ClassGroup ↔ Student**: Students can be in multiple classes
- **Course ↔ Teacher**: Teachers can teach multiple courses

### Foreign Key Relationships
- **Student → Attendance**: One student has many attendance records
- **Teacher → Course**: One teacher can teach multiple courses
- **Course → ClassGroup**: One course can have multiple class groups
- **Student → Invoice**: One student can have multiple invoices

## Model Methods

### Student Model Methods
- `get_age()`: Calculates student age from birth date
- `get_academic_year_display()`: Returns human-readable academic year
- `is_active_student()`: Checks if student has recent attendance

### Teacher Model Methods
- `get_active_courses()`: Returns currently taught courses
- `get_total_students()`: Counts total students across all classes
- `calculate_workload()`: Calculates teaching workload

### Course Model Methods
- `get_enrolled_count()`: Returns number of enrolled students
- `is_full()`: Checks if course reached maximum capacity
- `get_remaining_capacity()`: Calculates available spots

### Attendance Model Methods
- `get_monthly_attendance()`: Returns attendance summary for a month
- `get_attendance_rate()`: Calculates attendance percentage

## Model Choices

### Gender Choices
- `M`: Male
- `F`: Female

### Marital Status Choices
- `S`: Single
- `M`: Married
- `D`: Divorced
- `W`: Widowed

### Academic Year Choices
- `pre_primary`: Pre-Primary
- `primary_1` to `primary_6`: Primary levels 1-6
- `middle_1` to `middle_3`: Middle school levels 1-3
- `high_1` to `high_3`: High school levels 1-3
- `university_1` to `university_4`: University years 1-4
- `graduate`: Graduate

### Attendance Status Choices
- `P`: Present
- `A`: Absent
- `L`: Late

### Invoice Status Choices
- `Paid`: Fully paid
- `Unpaid`: Not paid
- `Partial`: Partially paid

## Database Constraints

### Unique Constraints
- Student national ID
- Teacher national ID
- Student attendance per date per class

### Check Constraints
- Phone numbers must be exactly 11 digits
- National IDs must be exactly 14 digits
- Amounts must be positive
- Dates must be logical (end > start, due > issue)

## Indexes

The database automatically creates indexes for:
- All foreign key fields
- Frequently queried fields (name, dates)
- Unique constraint fields

## Soft Deletes

Models use timestamp fields (`created_at`, `updated_at`) for tracking but do not implement soft deletes. Records are permanently deleted.

## Data Integrity

- All foreign key relationships are enforced
- Required fields are validated at model and form level
- Business logic is implemented in model methods and clean() methods
