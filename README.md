# miniAspire

## Overview

This is a simple Django application with Django Rest Framework and Django OAuth Toolkit. It simulates a loan application and repayment system.

## How to Run

1. Ensure Docker is installed on your machine. If it isn't, you can download it [here](https://www.docker.com/products/docker-desktop).

2. Open a terminal and navigate to the root directory of this project.

3. Create a `.env` file in the project root directory and set the following environment variables:
    ```
    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_PASSWORD=password
    ```
   These are the credentials for the pre-loaded superuser in the application.

4. Build the Docker image by running:
    ```
    docker build -t mini_aspire .
    ```
   This will create a Docker image named `mini_aspire`.

5. Once the image is built, you can run it using:
    ```
    docker run --env-file .env -p 8000:8000 mini_aspire
    ```
   This will start the Django application on port 8000. 

6. Navigate to `http://localhost:8000` in your web browser to interact with the application.

## Admin User

The application is pre-loaded with a superuser. The username and password for this user are set via the `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD` environment variables in the `.env` file. You can use this user to interact with the Django admin interface.

## Note
