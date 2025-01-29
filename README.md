# Academic Issue Tracking System (AITS)

A web-based platform that allows Makerere University students to log issues related to academic records (e.g., missing marks, appeals, corrections).

## Features

- User Roles and Permissions:
  - Students can log issues and view their status
  - Academic Registrar can review issues, resolve them, or assign them to relevant lecturers
  - Lecturers/Heads of Departments can resolve assigned issues and update statuses

- Issue Management:
  - Students can provide relevant details (course code, issue type)
  - Issues are categorized into "missing marks," "appeals," or "corrections"
  - File attachments support

- Notifications:
  - Email or in-app notifications for status changes
  - Alerts for overdue or unresolved issues

- Dashboard:
  - Personalized dashboard for each user role
  - Display relevant tasks and updates

- Audit Trail:
  - Maintain a log of actions performed on each issue

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ClaireAgaba/aits.git
cd aits
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create test users:
```bash
python manage.py setup_test_users
```

6. Run the development server:
```bash
python manage.py runserver
```

## Test Users

1. Student Account:
   - Username: `student1`
   - Password: `testpass123`

2. Lecturer Account:
   - Username: `lecturer1`
   - Password: `testpass123`

3. Academic Registrar Account:
   - Username: `registrar1`
   - Password: `testpass123`

## Technology Stack

- Backend: Django
- Database: SQLite (development) / PostgreSQL (production)
- Frontend: Bootstrap 5
- Authentication: Django Authentication System

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
