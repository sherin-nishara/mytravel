# Travel Booking Web App

This is a Django-based travel booking application where users can:

- Register, login, update profile
- View available travel options
- Book tickets and manage their bookings

## Technologies Used
- Python 3.x
- Django 4.x
- SQLite (for DB)
- Bootstrap 5 (for UI)

## Features
- User auth (login/register)
- Admin panel
- Travel filters + booking system
- Cancel bookings
- Responsive UI

## Setup Locally

```bash
git clone https://github.com/YOUR-USERNAME/travel-booking.git
cd travel-booking
python -m venv env
env\Scripts\activate  # or source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
