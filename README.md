# Library Management App

## Local deployment (Ubuntu)

1. Make sure that postgresql service is running on port 5432

2. To check if service is launched, run the following in the terminal:\
``systemctl status postgresql``

3. PostgreSQL database with the following credentials should be created before launching the project:\
NAME: 'library_management'\
USER: 'postgres'\
PASSWORD: 'postgres'

4. Make sure that poetry is installed, otherwise run:\
``pip install poetry``

5. Install necessary dependencies specified in pyproject.toml and poetry.lock (you should be in project folder):\
``poetry install``

6. Run migrations:\
``poetry run python manage.py migrate``

7. Start dev server\
``poetry run python manage.py runserver``

8. To run tests:\
``poetry run python manage.py test``

9. To run a specific test:\
``poetry run python manage.py test <path_to_specific_test>``\
e.g.:
``poetry run python manage.py test book.tests.tests.PrivateBookApiTests.test_list_books_filtered_success``

10. To run tests with coverage report:\
``coverage run --source='.' manage.py test``\
To see test coverage result:\
``coverage report``\
or\
``coverage html``
