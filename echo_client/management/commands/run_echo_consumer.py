import logging
from echo_client.echo_client import EchoClient
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start Echo consumer'

    def handle(self, *args, **options):
        echo_client = EchoClient()
        try:
            logger.info("Starting Echo Listener")
            echo_client.start_consuming()
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Consumer stopped by user'))
        except Exception as e:
            logger.error(f"Consumer failed: {e}")
            self.stdout.write(self.style.ERROR(f'Consumer failed: {e}'))