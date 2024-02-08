# WebbiSkools Quiz Management System

This project is a database-driven website designed to manage quizzes consisting of multiple-choice questions and their associated answers. The website's capabilities are accessible to known users with different levels of permissions.

Viewing and Editing:
- A user with Restricted permission can select a quiz and view all the questions in that quiz.
- A user with View permission can select and view a quiz, as well as select a question to see the associated answers.
- A user with Edit permission can select a quiz, view questions and answers, and make the following changes:
  - Create new quizzes and delete existing ones.
  - Add and delete questions at any point in the numerical sequence of a quiz (which may cause re-numbering).
  - Edit the text of any question.
  - Add and delete answers to any question (which may cause re-indexing).
  - Edit the text of any answer.

## Database Management

The database is stored in SQLite format and is located under the `database.db` file.

Included in this module is a Python script `script_bootstrap_data.py` that includes some sample data and 3 pre-defined logins:
- admin:password with the role Editor
- teacher:password with the role Viewer
- student:password with the role Restricted

To create a new user, you can run the `script_create_user.py` script.

It is recommended to use a tool such as SQLite Browser (https://sqlitebrowser.org/) to manage data in the database, as user management is not included in this project.

## Environment Variables

Environment variables can be set in a .env file,

SECRET_KEY: This variable represents the secret key used for sessions.
It should be a secure randomly generated string. If not set, a random key
will be generated each time the frontend is run, which will result in users
being logged out.

Example:
SECRET_KEY = cc071e39f8c2bfcbac5269bfc77021d3

## Deployment Instructions

Note: Node.js and npm are required to build the frontend. Make sure you have them installed.
If you don't have Node.js installed, you can download it from https://nodejs.org/.
npm (Node Package Manager) is bundled with Node.js and is used to install project dependencies.
To install the project dependencies, run the command `npm install` in the project root directory.

1. To build the Vue project, follow these steps:
 - Navigate to the web folder.
 - Run the command `npm run build`.
 - This will build the Vue project.

Note: Python is required to run the frontend. Make sure you have them installed.
If you don't have Python installed, you can download it from https://www.python.org/.
pip is bundled with Python and is used to install project dependencies. To install the
required dependencies, run the command `pip install -r requirements.txt`.

2. To deploy the Quart application, follow these steps:
  - Navigate to the backend folder.
  - Run the command `quart run`.
  - This will serve the frontend.
