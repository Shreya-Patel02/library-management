# library-management
## Overview
This project is a Library Management System built using Django and Django REST Framework (DRF). It provides RESTful APIs for managing books, members, and loan transactions. The application supports operations for:

- Managing books (adding, updating, deleting, viewing)
- Managing members (registering, updating, deleting, viewing)
- Managing loan records (borrowing, returning books, tracking overdue fines)
- Search functionality for books by title, author, or genre
- Overdue management for calculating and applying fines when books are returned after the due date.

## Features
### Book Management:
- Retrieve a list of all books
- Retrieve details of a specific book
- Add a new book
- Update book details
- Remove a book from inventory
### Member Management:
- Retrieve a list of all members
- Retrieve details of a specific member
- Register a new member
- Update member details
- Remove a member
### Loan Management:
- Borrow a book
- Return a book
- Retrieve all loans
- Retrieve details of a specific loan
### Search Functionality:
- Search for books by title, author, or genre using query parameters
### Overdue Management:
- Calculate and apply overdue fines based on the due date and current date
### Business Logic:
- Ensure members cannot borrow more books than available copies
- Ensure loans are not created for non-existent books or members

## Installation
### 1. Clone the repository:
git clone https://github.com/Shreya-Patel02/library-management.git
cd library-management-system

### 2. Create a virtual environment (optional but recommended):
python3 -m venv venv
source venv/bin/activate  # For Windows use: venv\Scripts\activate

### 3. Install dependencies:
pip install -r requirements.txt

### 4. Set up PostgreSQL:
- Install PostgreSQL on your machine if you haven't already.
- Create a database for the project (e.g., library_management).

### 5. Configure Database Settings:
- In settings.py, set up your database connection
- DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_management',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

### 6. Migrate the database:
python manage.py migrate

### 7. Run the development server:
python manage.py runserver


## API Endpoints Documentation
https://documenter.getpostman.com/view/40586989/2sAYJ3Fh75



































