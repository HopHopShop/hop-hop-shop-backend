## Technologies Used

This project is developed using the following technologies:

- Django: Python-based web framework for building web applications.
- Database: PostgreSQL
- Redis: In-memory data structure store, used as a message broker for Celery and for caching.
- Celery: Distributed task queue for handling asynchronous and scheduled tasks.
- Swagger: Tool for documenting and testing RESTful APIs.

## Usage Instructions

Python must be already installed.

1. **Installation:**
    - Clone the repository to your local machine `https://gitlab.valuebridge.solutions/team-challenge/e-com/e-com-back.git`.
    - Create virtual environment `python3 -m venv venv`
    - Install the required dependencies using `pip install -r requirements.txt`.

2. **Running:**
    - Apply migrations `python manage.py migrate`
    - Start the server with `python manage.py runserver`.
    - Access the store via `http://localhost:8000` in your web browser.

3. **Registration/Login:**
    - To access all functionalities of the project, create super user and log in to your account.

## Configure environment variables

Before running the project, create a `.env` file based on the `env.sample` file and fill in all the necessary variables.

### Steps to Create the .env File

1. Copy the `env.sample` file and rename it to `.env`:
    ```sh
    cp env.sample .env
    ```

2. Open the `.env` file in a text editor and fill in the variable values.

## Docker

To run the project using Docker Compose:
- Start the containers: `docker-compose up --build`
- Access the application at http://localhost:8000

## Developer Commands

- `python manage.py makemigrations`: Create database migrations.
- `python manage.py migrate`: Apply migrations to the database.
- `python manage.py createsuperuser`: Create a site administrator.

