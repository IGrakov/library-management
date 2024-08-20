# Library Management App

## Local deployment

1. Make sure that postgresql service is running on port 5432

2. To check if service is launched, run the following in the terminal:
``systemctl status postgresql``

3. PostgreSQL database with the following credentials should be created before launching the project:
NAME: 'library_management'
USER: 'postgres'
PASSWORD: 'postgres'

4. Make sure that poetry is installed, otherwise run:
``pip install poetry``

5. Install necessary dependencies specified in pyproject.toml and poetry.lock (you should be in project folder):
``poetry install``

6. Run migrations:
``poetry run python manage.py migrate``

7. Start dev server:
``poetry run python manage.py runserver``

8. To run tests:
``poetry run python manage.py test``