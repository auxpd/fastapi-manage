from core.config import settings

# Broker settings.
broker_url = settings.CELERY_BROKER

# Using the database to store task state and results.
result_backend = settings.CELERY_BACKEND

# The name of the default queue used by .apply_async if the message has no route or no custom queue has been specified.
task_default_queue = 'celery'

# A white-list of content-types/serializers to allow.
accept_content = {'json'}

# A white-list of content-types/serializers to allow for the result backend.
result_accept_content = {'json'}

# Configure Celery to use a custom time zone. The timezone value can be any time zone supported by the pytz library.
timezone = settings.TIMEZONE

# Exact same semantics as imports, but can be used as a means to have different import categories.
include = ['tasks.tasks']
