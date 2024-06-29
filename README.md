# @solve-me

# Overview

SolveMe is an API for a quiz-based application built with FastAPI. It allows users to register, log in, retrieve questions based on their score level, submit answers, and track their progress. The application supports user roles (user and admin) with different levels of access to the API endpoints.

# Features

User Authentication and Authorization: Signup, login, and secure access to endpoints with JWT tokens.
* Question Management: CRUD operations for questions.
* Submission Management: Submit answers to questions and retrieve submission history.
* User Management: View and manage user accounts.

# Getting Started

Prerequisites:
* Python 3.7+
* MySQL Database

# Installation

**Clone the repository:**
> git clone https://github.com/abdullahajam7/solve-me.git

**Set up a virtual environment:**
>  python -m venv venv

then

>  source venv/bin/activate

On Windows use

> `venv\Scripts\activate`

**Install the required dependencies:**
> pip install -r requirements.txt

**Set up the database:**
* Create a MySQL database.
* Update the database.py file with your database connection details.


# Running the Application:
**Start the FastAPI server:**
> uvicorn main:app --reload


**Access the API documentation:**
Open your browser and go to the Swagger Documentation <http://127.0.0.1:8000/docs> to see the interactive API documentation.


**Project Structure**
* main.py: The entry point of the application. Sets up the FastAPI app and includes routers.
* models.py: SQLAlchemy models for the database tables.
* database.py: Database connection setup.
* routers/: Contains the different route files for authentication, users, questions, and submissions.
* auth.py: Handles user authentication and authorization.
* users.py: User-related endpoints.
* questions.py: Question-related endpoints.
* submissions.py: Submission-related endpoints.


# API Endpoints
**Authentication**
* POST /auth/signup: Create a new user.
* POST /auth/login: Log in and obtain a JWT token.

**Users**
* GET /users/: Get all users (Admin only).
* GET /users/{id_user}: Get a user by ID (Admin only).
* PUT /users/password: Update the current user's password.
* DELETE /users/: Delete the current user's account.
* PUT /users/admin: Promote a user to admin (Admin only).

**Questions**
* GET /questions/all: Get all questions (Admin only).
* GET /questions/{id_question}: Get a question by ID (Admin only).
* GET /questions/: Get a question for the current user.
* POST /questions/: Add a new question (Admin only).
* PUT /questions/{id_question}: Update a question (Admin only).
* DELETE /questions/{id_question}: Delete a question (Admin only).

**Asked_Questions**
* GET /asked_questions/all: Get all asked_questions (Admin only).
* GET /asked_questions/: Get asked_questions for a specific game passed by params (Admin only).
* GET /asked_questions/{id_asked_question}: Get an asked_question by ID (Admin only).
* POST /asked_questions/submit: Submit an answer to the asked question.


**Games**
* GET /games/all: Get all games stats (Admin only).
* GET /games/: Get games stats for a specific id_user passed by params (Admin only).
* GET /games/{id_game}: Get a game stats by ID (Admin only).
* POST /games/: starts a game for the current logged in user.
