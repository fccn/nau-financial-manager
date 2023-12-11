# Gunicorn-django settings
bind = ["0.0.0.0:8000"]
name = "app"
python_path = "/app"

# Run
graceful_timeout = 90
timeout = 90
workers = 3

# Logging
# Using '-' for the access log file makes gunicorn log accesses to stdout
accesslog = "-"
# Using '-' for the error log file makes gunicorn log errors to stderr
errorlog = "-"
loglevel = "info"

# Handler that forces Gunicorn to print the current stack trace, when its worker timeout’s.
# This can happen when a request hangs waiting for an external service dependency, like when a
# database is too slow or can't connect to the S3 Bucket provider. The worker receives the SIGABRT
# signal from the Gunicorn parent process and this handler runs before the worker it stopped.
# Reference:
# https://stackoverflow.com/questions/15442361/dump-django-stack-trace-on-gunicorn-timeout
def worker_abort(worker):
    import traceback, io
    debug_info = io.StringIO()
    debug_info.write("Traceback at time of timeout:\n")
    traceback.print_stack(file=debug_info)
    worker.log.critical(debug_info.getvalue())
