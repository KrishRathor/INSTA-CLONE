# Insta-Clone

Welcome to Insta-Clone, a project aimed at replicating the functionality of Instagram using HTML, CSS, JavaScript, and Flask. This project allows you to create a web-based application that mimics some of the key features of Instagram.

## Table of Contents
- [Setup](#setup)
- [Features](#features)
- [Usage](#usage)
- [Contributing](#contributing)
  
## Setup
To get started with Insta-Clone, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/KrishRathor/INSTA-CLONE.git
    ```

2. Navigate to the project directory:

    ```bash
    cd INSTA-CLONE
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Run the Flask application:

    ```bash
    flask run --app app --debug
    ```

7. Open your web browser and visit `http://localhost:5000` to access Insta-Clone.

## Features
- User registration and authentication
- Posting photos and captions
- Like and comment on posts
- News feed
  
## Usage
Once the application is set up, you can use Insta-Clone by navigating to `http://localhost:5000` in your web browser. Create an account, log in, and start exploring the features such as posting photos, following other users, and interacting with posts in your news feed.

## Contributing
If you would like to contribute to Insta-Clone, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`.
3. Make your changes and commit them: `git commit -m "Description of changes"`.
4. Push your changes to your fork: `git push origin feature-name`.
5. Open a pull request.
