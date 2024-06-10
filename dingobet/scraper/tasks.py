# scraper/tasks.py

from celery import shared_task
from .TransfermarktClient import TransfermarktClient
from .live import parseLiveSoup

@shared_task
def run_my_scraper():
    client = TransfermarktClient()
    soup = client.getLiveSoup()
    if soup:
        parseLiveSoup(soup)
