FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY . /code/

# Expose the port for the Django project to run on
EXPOSE 8000

# Run the Djago project for development
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]