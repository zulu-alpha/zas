# Download and base the container
FROM ubuntu

# Copy the backup script and cron jobs over
ADD . /opt/backup

# Make the script's directory the current working directory
WORKDIR /opt/backup

# Allow the script to be executed
RUN chmod +x /opt/backup/backup.py

# Add the job to the cron
RUN crontab /opt/backup/backup_cron.txt

# Make the container run without closing
ENTRYPOINT ["cron", "-f"]