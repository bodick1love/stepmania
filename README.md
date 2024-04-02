# Stepmania Repository

Clone the repository:
git clone repository_url

Create a virtual environment:
python -m venv venv

Activate the virtual environment:
On Windows:
venv\Scripts\activate

On macOS and Linux:
source env/bin/activate

Install dependencies:
pip install -r requirements.txt

Navigate into the project directory:
cd stepmania

Apply migrations:
python manage.py migrate

Create a superuser (admin):
python manage.py createsuperuser

Run the development server:
python manage.py runserver
The server will start running at http://localhost:8000.

## Usage
1. Access the admin interface by navigating to http://localhost:8000/admin and logging in with the superuser credentials created earlier.
2. Use the admin interface to manage products, orders, etc.
3. Access the front-end of the store by navigating to http://localhost:8000.
