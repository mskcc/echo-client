import logging
from echo_client.messages import DeleteTask
from echo_client.echo_client import EchoClient
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Delete File command'

    def add_arguments(self, parser):
        parser.add_argument("--source", type=str)

    def handle(self, *args, **options):
        source = options["source"]
        echo_client = EchoClient()
        try:
            message = DeleteTask(source)
            echo_client.publish(message)
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Consumer stopped by user'))
        except Exception as e:
            logger.error(f"Error: {e}")