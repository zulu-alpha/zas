# Download and base the container off of a pure Python 3.5 image
FROM python:3.5

# Copy everything in the project folder to a new /guestbook folder in the directory
ADD . /opt/migrate

# Make that new directory the new working directory
WORKDIR /opt/migrate

# pip install what is in the requirements.txt file
RUN pip install -r requirements.txt

# Run the flask app
ENTRYPOINT ["python", "/opt/migrate/migrate.py"]
