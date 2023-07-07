# BlogApp

Welcome to BlogApp! This is a web application for creating and managing your own blog.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

BlogApp is a powerful tool for bloggers to publish and manage their content. It provides an intuitive and user-friendly
interface for creating, editing, and organizing blog posts.

## Features

- User authentication: Securely register, login, and manage your account.
- Create blog posts: Write and publish articles with a rich text editor.
- Edit and delete posts: Easily update your posts or remove them if needed.
- Categorize posts: Organize your content by assigning categories and tags.
- Comment system: Engage with your readers through comments on your posts.
- Search functionality: Quickly find posts by title, category, or tags.

## Installation

To install and run BlogApp locally, follow these steps:

1. Clone the repository:
    ```sh
      git clone https://github.com/evil-kekc/BlogApp.git
    ```

2. Activating the virtual environment
   * Using Linux
   ```shell
    sudo apt-get install python3-venv
    python3 -m venv myenv
    source myenv/bin/activate
   ```
   
   * Using Windows
   ```shell
    pip install virtualenv
    python -m venv myenv
    myenv\Scripts\activate
   ```

3. Install the dependencies:
    ```sh
      cd BlogApp
      pip install -r requirements.txt
    ```
4. Configure the environment variables:

   Create a `.env` file in the project root and set the following variables:
   ```dotenv
      SECRET_KEY=<YOUR_SECRET_KEY_HERE>
      ADMIN_GMAIL=<YOUR_EMAIL_APP_HERE>
      ADMIN_GMAIL_PASSWORD=<YOUR_EMAIL_APP_PASSWORD_HERE>
      
      DATABASE_NAME=<YOUR_DB_NAME_HERE>
      POSTGRES_USER_NAME=<YOUR_POSTGRES_USERNAME_HERE>
      POSTGRES_USER_PASSWORD=<YOUR_POSTGRES_PASSWORD_HERE>
      POSTGRES_HOST=<YOUR_POSTGRES_HOST_HERE>
      POSTGRES_POST=<YOUR_POSTGRES_PORT_HERE>
   ```

5. Start the application:
   * Using Docker:
   ```shell
   docker build -t blogapp .
   docker run -p 8000:8000 -d blogapp
   ```
   
   * Without Docker:
   ```shell
   ./manage.py runserver 
   ```

6. Access the application in your browser at `http://localhost:8000`.

## Usage

1. Register a new account or log in with your existing credentials.
2. Create a new blog post by clicking on the `New Post` button.
3. Fill in the necessary details, such as title, content, categories, and tags.
4. Click `Publish` to make your post live on the blog.
5. Explore other features, such as editing posts, adding comments, and using the search functionality.

## Contributing

Contributions to BlogApp are welcome! If you find a bug or want to suggest an enhancement, please open an issue in
the [Issue Tracker](https://github.com/evil-kekc/BlogApp/issues). If you'd like to contribute code, please follow these
steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request to the main repository.

Please ensure that your code follows the project's coding style and includes appropriate tests.
**Make sure you** have [Docker](https://www.docker.com) installed on your system in order to use it to build and run the application.
