# @solve-me

# Overview

SolveMe is an API for a quiz-based application built with FastAPI. It allows users to register, log in, retrieve questions based on their score level, submit answers, and track their progress. The application supports user roles (user and admin) with different levels of access to the API endpoints._


# Features

User Authentication and Authorization: Signup, login, and secure access to endpoints with JWT tokens.
*Question Management: CRUD operations for questions.
*Submission Management: Submit answers to questions and retrieve submission history.
*User Management: View and manage user accounts.


# Getting Started

Prerequisites:
*Python 3.7+
*MySQL Database


# Installation

**Clone the repository:**
* git clone https://github.com/abdullahajam7/solve-me.git
* Set up a virtual environment: python -m venv venv
* source venv/bin/activate  # On Windows use `venv\Scripts\activate`

**Install the required dependencies:**
pip install -r requirements.txt

**Set up the database:**
* Create a MySQL database.
* Update the database.py file with your database connection details.


# Running the Application:
**Start the FastAPI server:**
uvicorn main:app --reload


**Access the API documentation:**
Open your browser and go to http://127.0.0.1:8000/docs to see the interactive API documentation.


**Project Structure**
* main.py: The entry point of the application. Sets up the FastAPI app and includes routers.
* models.py: SQLAlchemy models for the database tables.
* database.py: Database connection setup.
* routers/: Contains the different route files for authentication, users, questions, and *submissions.
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
* GET /users/{user_id}: Get a user by ID (Admin only).
* PUT /users/password: Update the current user's password.
* DELETE /users/: Delete the current user's account.
* PUT /users/admin: Promote a user to admin (Admin only).

**Questions**
* GET /questions/all: Get all questions (Admin only).
* GET /questions/{question_id}: Get a question by ID (Admin only).
* GET /questions/: Get a question for the current user.
* POST /questions/: Add a new question (Admin only).
* PUT /questions/{question_id}: Update a question (Admin only).
* DELETE /questions/{question_id}: Delete a question (Admin only).

**Submissions**
* GET /submissions/all: Get all submissions (Admin only).
* GET /submissions/: Get submissions for a specific game and user (Admin only).
* GET /submissions/{submission_id}: Get a submission by ID (Admin only).
* POST /submissions/submit: Submit an answer to the asked question.
