# Download and base the container
FROM python:3.5

# Copy the backup script and cron jobs over
ADD . /opt/restore

# Make the script's directory the current working directory
WORKDIR /opt/restore

# Make the container run without closing
ENTRYPOINT ["python3", "/opt/restore/restore.py"]