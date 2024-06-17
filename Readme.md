# Birthday Reminder App

This is a Flask application for managing and reminding users of birthdays. The app allows users to register, log in, add, edit, and delete birthday entries. There is also an admin-only section for managing users.

## Features

- Allow users to add friends' birthdays and manage entries via a user-friendly interface.
- Send automated birthday messages at 7:30 AM EST using a Celery beat schedule and Redis server for efficient local communication.
- Ensure reliable notifications and a seamless user experience through the integration of Celery and Redis for task management and message scheduling.
- User registration and login
- Add, edit, and delete birthday entries
- Admin-only section for managing users
- CKEditor for rich text input
- Bootstrap 5 integration for styling

## Technology Used for Birthday Reminder Application

- **Programming Language:** Python
- **Frameworks:** Flask
- **Database:** SQLAlchemy local PostgreSQL deployed
- **Task Queue:** Celery
- **Message Broker:** Redis
- **Packages:** FlaskForm, wtforms, twilio

## Requirements

- Python 3.7+
- Flask
- Flask-Bootstrap
- Flask-CKEditor
- Flask-Login
- Flask-SQLAlchemy
- Werkzeug
- SQLAlchemy

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/osstd/The-Birthday-Wisher-.git
    cd birthday_wisher
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables. Create a `.env` file in the project root directory and add the following:

    ```env
    F_KEY=your_secret_key
    DB_URI=your_database_uri (default: sqlite:///birthdays.db)
    ```

    Replace `your_secret_key` with a secret key for your Flask application. If you are using a different database than the default SQLite, replace `your_database_uri` with the appropriate database URI.

5. Run the application:

    ```bash
    flask run
    ```

## Usage

### Routes

- `/` : Home page
- `/register` : User registration page
- `/login` : User login page
- `/logout` : User logout
- `/add` : Add a new birthday entry (requires login)
- `/save` : Save a new birthday entry (requires login)
- `/edit-birthday/<int:birthday_id>` : Edit an existing birthday entry (requires login)
- `/delete/<int:birthday_id>` : Delete a birthday entry (requires login)
- `/delete-user/<int:user_id>` : Delete a user (admin only, requires login)
- `/user` : User profile page (requires login)

### Admin-Only Features

The application includes a decorator `@admin_only` that restricts access to certain routes to the admin user (user with ID 1).

### Forms

- `RegisterForm` : For user registration
- `LoginForm` : For user login
- `EditBirthdayForm` : For editing birthday entries

## Database Models

- `User` : Represents a user in the application
- `Birthdays` : Represents a birthday entry associated with a user

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

