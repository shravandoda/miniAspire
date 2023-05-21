# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Add current directory code to /app in container
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set environment variables
ENV DJANGO_SUPERUSER_USERNAME ${DJANGO_SUPERUSER_USERNAME}
ENV DJANGO_SUPERUSER_PASSWORD ${DJANGO_SUPERUSER_PASSWORD}

# Run startup.py and then start the Django server
CMD ["sh", "-c", "python startup.py && python manage.py runserver 0.0.0.0:8000"]
