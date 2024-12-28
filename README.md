Customer Management API

Project Overview

The Customer Management API is a professional-grade application developed using Flask. It provides secure endpoints for user authentication and customer management, including balance updates and customer data retrieval. Designed for scalability and ease of integration, this API is equipped with robust JWT-based authentication and adheres to best practices in modern API development.

Features

User Authentication: Secure registration and login using hashed passwords and JWT tokens.

Customer Management: Add, update, and retrieve customer data.

Data Security: All sensitive endpoints are protected using JWT-based authentication.

Extensibility: Built with modularity in mind to allow for future feature additions.

Setup Instructions

Prerequisites

Python: Ensure Python 3.8+ is installed.

SQLite: No additional setup required (SQLite is included with Python).

Installation Steps

1. Clone the Repository:

git clone https://github.com/your-repo/CustomerManagementAPI.git
cd CustomerManagementAPI

2. Set Up a Virtual Environment:

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3. Install Dependencies:

pip install -r requirements.txt

4. Initialize the Database:
The database is automatically initialized using db.create_all() when the application starts for the first time. Alternatively, if you want to manually initialize the database, use the following SQL script:

-- Initialize users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Initialize customers table
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    balance REAL DEFAULT 0.0
);

5. Run the Application:

python app.py
The application will be available at http://127.0.0.1:5000.

API Endpoints

User Authentication

Register a New User

Endpoint: POST /register

Payload: 
{
  "username": "test_user",
  "password": "test_pass"
}
Response:

{"message": "User registered successfully"}

User Login

Endpoint: POST /login

Payload:
{
  "username": "test_user",
  "password": "test_pass"
}

Response:
{"token": "YOUR_JWT_TOKEN"}

Customer Management

Retrieve All Customers

Endpoint: GET /customers

Headers:
Authorization: Bearer YOUR_JWT_TOKEN

Response:
[
  {"id": 1, "name": "Customer 1", "balance": 100.0},
  {"id": 2, "name": "Customer 2", "balance": 200.0}
]

Top Up Customer Balance

Endpoint: POST /customers/<id>/topup

Headers:
Authorization: Bearer YOUR_JWT_TOKEN

Payload:
{
  "amount": 50.0
}

Response:
{
  "message": "Balance updated successfully",
  "new_balance": 150.0
}

Testing the API

You can test the API using PowerShell, cURL, or a Python script:

Example Using PowerShell

Test /register:
Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:5000/register" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username": "test_user", "password": "test_pass"}'

  Test /login:
  $response = Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:5000/login" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"username": "test_user", "password": "test_pass"}'

  $token = $response.token

  Test/customers/1/topup:
  Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:5000/customers/1/topup" `
  -Headers @{ "Authorization" = "Bearer $token"; "Content-Type" = "application/json" } `
  -Body '{"amount": 50.0}'

Dependencies

The project requires the following dependencies:

Flask

Flask-SQLAlchemy

Flask-Migrate

Flask-Bcrypt

Flask-JWT-Extended

Install them using the requirements.txt file:

pip install -r requirements.txt