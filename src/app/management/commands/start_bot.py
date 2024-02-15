from django.core.management.base import BaseCommand

from app.internal.bot import start_bot


class Command(BaseCommand):
    help = "Command to launch the telegram bot"

    def handle(self, *args, **options):
        start_bot()
