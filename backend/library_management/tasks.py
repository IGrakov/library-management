from celery import shared_task
from django.utils import timezone


@shared_task()
def test_task() -> None:
    print(f"Test task @{timezone.now()}")
