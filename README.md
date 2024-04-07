# Flask Blog Application

This Flask-based blog application allows users to create, edit, and delete blog posts. Users can register for an account, log in, and then create new blog posts containing titles and content. The application provides functionality to edit existing blog posts and delete them if needed. It utilizes SQLAlchemy as the ORM for database operations. With its user-friendly interface and robust features, it provides a seamless experience for bloggers to manage their content.

## Features

- User registration and login
- Create, edit, and delete blog posts
- Database operations with SQLAlchemy
- User authentication with Flask-Login

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/shubhamvisare22/Blog-App-Flask.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

4. Run the application:
   ```
   flask run
   ```

## Usage

- Visit the application in your web browser.
- Register for an account or log in if you already have one.
- Create, edit, or delete blog posts from the dashboard.
- Log out when finished.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests to suggest improvements or fix bugs.


