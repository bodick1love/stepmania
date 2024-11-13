# Stepmania Repository

1. Clone the repository:
   ```
   git clone https://github.com/bodick1love/stepmania
   ```
   
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
   
3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```
   
4. Navigate into the project directory:
   ```
   cd stepmania
   ```

5. Install dependencies:
   ```
   pip install -r requirements.txt
   
8. Run the development server:
   ```
   python manage.py runserver
   ```

   The server will start running at http://localhost:8000.

## Usage
1. Access the admin interface by navigating to http://localhost:8000/admin and logging in with the superuser credentials created earlier.
2. Use the admin interface to manage products, orders, etc.
3. Access the front-end of the store by navigating to http://localhost:8000.
