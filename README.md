# Mini Loan request Platform

This is the **backend** of the Mini Loan Request Platform, built with **Flask** 
It provides the user to register and apply for a small loan


##  Features
- RESTful API with JSON responses.
- Database migrations using Alembic/Flask-Migrate
- CORS enabled for frontend integration (React or any other client)
- User management (create, read).
- Loan management(create)

---

## Technologies Used

- **Flask** – Web framework
- **Flask-RESTful** – For building REST APIs
- **Flask-Migrate** – Database migrations
- **SQLAlchemy** – ORM for database interaction
- **Flask-CORS** – Handle cross-origin requests

---

## Installation & Setup

1. Navigate to the server folder:
```bash
   cd server
```

2. Install dependencies
```bash
pipenv install flask flask-migrate flask-bcrypt flask-sqlalchemy sqlalchemy-serializer python-dotenv
```

3. Enter into the virtual environment
```bash
npm pipenv shell
```

4. Set the port of the application
```bash
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
```

5. Create the models and run
```bash
flask db init
flask db migrate -m"Initial migration"
flask db upgrade head
```

6. Create the sample data and run
```bash
python seed.py
```

7. Run the application
```bash
python app.py
```

The frontend is set to run on (http:127.0.0.1:5555)

## Project Structure
├── Server/
│   ├── migrations/
│   ├── models.py
│   ├── app.py
│   ├── seed.py
│   ├── config.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── user_routes.py
│   │   ├── loan_routes.py
│   ├── Pipfile / Pipfile.lock
│   └── instance/
│       └── loans.db
│
├── README.md
└── .gitignore


---


## API Endpoints
### Users
GET /users – Get all users
POST /users – Create a new user

### Trips
GET /loans/<id> – Get a specific loan

---y

## 📜 License

This project is licensed under the **MIT License**.

© 2025 Cheryl Mbani
