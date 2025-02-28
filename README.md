# Yacht Booking Backend

This is the backend of the **Yacht Booking System**, built using the Django REST Framework.

## Features
- User authentication and management
- Vendor and yacht management
- Booking and payment integration
- Secure API endpoints with authentication

## Prerequisites
Before you begin, ensure you have the following installed:
- Python 3.x
- pip (Python package manager)
- virtualenv (optional but recommended)
- SQLite (or another preferred database)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/ntNayan23/Yatch_Backend.git
```
## 2. Open Yatch_Backend in Vscode 
## 3. Create a virtual Environment and activate the environment
```bash
    python -m venv venv  # Create a virtual environment
    source venv/bin/activate  # Activate it (Mac/Linux)
    venv\Scripts\activate  # Activate it (Windows)
```
### 4. Install Dependencies
    cd yatchbackend (change the  directory)
    pip install -r requirements.txt 
### 5. Apply Migrations
    python manage.py migrate
### 6. Run the Development Server
    python manage.py runserver
Your Django API will be available at: http://127.0.0.1:8000/
### To Test Api go to the  swagger Documentation 
    http://127.0.0.1:8000/swagger/


