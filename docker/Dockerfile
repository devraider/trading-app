FROM python:3.12-alpine

WORKDIR /app

# Copy project files into the container
COPY src /app
COPY ./requirements.txt /app

## Install system dependencies and Python requirements
#RUN apt-get update && \
#    apt-get install -y libpq-dev gcc
RUN pip install --no-cache-dir -r requirements.txt

# Django apply migrations
RUN python manage.py migrate

# Collect static files
#RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Bootstrap app (By default starts in development mode)
#CMD ["gunicorn", "trading.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["python3", "manage.py",  "runserver", "0.0.0.0:8000"]
