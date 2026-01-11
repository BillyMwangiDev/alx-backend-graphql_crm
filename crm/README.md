# CRM App - Celery Setup Guide

This guide explains how to set up and run Celery tasks for the CRM application.

## Prerequisites

- Python 3.11+
- Redis server
- Django project with all dependencies installed

## Installation Steps

### 1. Install Redis

#### On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

#### On macOS:
```bash
brew install redis
brew services start redis
```

#### On Windows:
Download and install Redis from: https://github.com/microsoftarchive/redis/releases

Or use WSL (Windows Subsystem for Linux) and follow Ubuntu instructions.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- celery
- django-celery-beat
- redis

### 3. Run Migrations

Since django-celery-beat requires database tables, run migrations:

```bash
python manage.py migrate
```

### 4. Start Redis Server

Make sure Redis is running:

```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG
```

If Redis is not running, start it:

```bash
# On Linux/macOS
redis-server

# On Windows (if installed)
redis-server
```

### 5. Start Celery Worker

In a terminal, start the Celery worker:

```bash
celery -A crm worker -l info
```

This will start a worker process that executes tasks.

### 6. Start Celery Beat

In another terminal, start Celery Beat (the scheduler):

```bash
celery -A crm beat -l info
```

This will schedule and trigger periodic tasks according to the schedule defined in `crm/settings.py`.

## Scheduled Tasks

The CRM report is scheduled to run every Monday at 6:00 AM. The schedule is defined in `crm/settings.py`:

```python
CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
```

## Verifying the Setup

### Check Logs

The CRM report logs are written to `/tmp/crm_report_log.txt`. To view the logs:

```bash
# View the log file
cat /tmp/crm_report_log.txt

# Or tail to see latest entries
tail -f /tmp/crm_report_log.txt
```

The log format is:
```
YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
```

### Manual Task Execution

You can manually trigger the report task for testing:

```bash
python manage.py shell
```

Then in the shell:
```python
from crm.tasks import generate_crm_report
generate_crm_report.delay()  # Async execution
# or
generate_crm_report()  # Synchronous execution for testing
```

## Troubleshooting

### Redis Connection Error

If you see connection errors, ensure Redis is running:
```bash
redis-cli ping
```

### Task Not Executing

1. Ensure both Celery worker and Celery Beat are running
2. Check that the Django development server is running (for GraphQL queries)
3. Verify the schedule in `crm/settings.py`
4. Check Celery worker logs for errors

### GraphQL Query Errors

Ensure the Django development server is running on `http://localhost:8000` so that GraphQL queries can be executed.

## Production Considerations

For production deployments:

1. Use a process manager like supervisord or systemd to manage Celery processes
2. Configure Redis persistence and backup
3. Set up monitoring for Celery workers
4. Use a message broker like RabbitMQ for better reliability (optional)
5. Configure proper logging and error handling
6. Set up alerts for task failures
