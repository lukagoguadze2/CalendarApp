# University Course Scheduler

This project is designed to simplify student life by providing a centralized platform for managing university courses, schedules, and evaluations. With features tailored to universities, faculties, courses, and groups, it helps students stay organized and informed about their academic commitments.

---

## Key Features

1. **University Management**: 
   - Lists universities, faculties, and their respective courses.

2. **Course Scheduling**:
   - Displays course schedules by university, faculty, and group.
   - Includes a calendar view to easily visualize schedules and evaluation lectures.

3. **Group Management**:
   - Enables students to view course schedules for their specific group.

4. **Event Notifications**:
   - Automatically sends email reminders for evaluation lectures or other events scheduled the next day.

---

## Prerequisites

1. Python 3.8+
2. Django 4.2+
3. Redis (for Celery task management)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lukagoguadze2/CalendarApp.git
   cd CalendarApp
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt # For development
   ```

4. Set up the `.env` file:
   Create a `.env` file in the root directory and add the following variables:
   ```env
   SECRET_KEY='your-secret-key'
   EMAIL_HOST_USER='your-email@example.com'
   EMAIL_HOST_PASSWORD='your-email-password'
   CELERY_BROKER_URL='redis://localhost:6379/0'
   CELERY_RESULT_BACKEND='redis://localhost:6379/0'
   ```

5. Apply migrations and populate the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py populate_test_data  # Optional: Populate the database with test data
   ```
   
   ### Note: Run the following command to populate the database with test data:
   ```bash
      python manage.py populate_test_data
   ```

6. Run the server:
   ```bash
   python manage.py runserver
   ```

---

## Using Redis and Celery

1. Install Docker Desktop if not already installed.

2. Start a Redis container:
   ```bash
   docker run -d --name redis -p 6379:6379 redis
   ```

3. Start the Celery worker:
   ```bash
   celery -A CalendarApp worker --loglevel=info
   ```

---

## Features Overview

### Calendar View
- **University**: Choose a university.
- **Faculty**: Select the faculty under the university.
- **Course**: View course schedules including groups.
- **Evaluation Lectures**: Marked prominently in the calendar.

### Email Reminders
- Automatically sends reminders to students about upcoming evaluation lectures.

---

## Contribution Guidelines

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit changes and push to your fork.
4. Create a pull request to the main repository.

---
