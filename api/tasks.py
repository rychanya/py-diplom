from celery import shared_task


@shared_task
def debug_task(request):
    print(f"Request: {request!r}")
