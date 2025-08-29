import logging
from echo_client.messages import CopyTask
from echo_client.echo_client import EchoClient
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Copy File command'

    def add_arguments(self, parser):
        parser.add_argument("--source", type=str)
        parser.add_argument("--destination", type=str)

    def handle(self, *args, **options):
        source = options["source"]
        destination = options["destination"]
        echo_client = EchoClient()
        try:
            message = CopyTask(source, destination)
            echo_client.publish(message)
        except Exception as e:
            logger.error(f"Error: {e}")