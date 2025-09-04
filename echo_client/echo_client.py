import pika
import json
import logging
from django.conf import settings
from importlib import import_module
from typing import Callable, Any, Dict
from echo_client.messages.message_factory import MessageFactory

logger = logging.getLogger(__name__)

class EchoClient(object):

    def __init__(self, connection_params: object = None, task_queue: str = "echo.task_queue",
                 confirmation_queue: str = "echo.confirmation_queue"):
        self._connection = None
        self._channel = None
        echo_settings = getattr(settings, 'ECHO_SETTINGS', {})
        self.task_queue = echo_settings.get("ECHO_TASK_QUEUE", task_queue)
        self.confirmation_queue = echo_settings.get("ECHO_CONFIRMATION_QUEUE", confirmation_queue)
        self.connection_params = connection_params or self._get_default_connection_params()

    def _get_default_connection_params(self):
        echo_settings = getattr(settings, 'ECHO_SETTINGS', {})
        username = echo_settings.get("USERNAME", "guest")
        password = echo_settings.get("PASSWORD", "guest")
        credentials = pika.PlainCredentials(
            username, password
        )
        return pika.ConnectionParameters(
            host=echo_settings.get('HOST', 'localhost'),
            port=echo_settings.get('PORT', 5672),
            virtual_host=echo_settings.get('VHOST', '/'),
            credentials=credentials,
            heartbeat=600,
            blocked_connection_timeout=300
        )

    def connect(self):
        if self._connection is None or self._connection.is_closed:
            self._connection = pika.BlockingConnection(self.connection_params)
            self._channel = self._connection.channel()
        return self._channel

    def publish(self, message):
        try:
            channel = self.connect()
            channel.queue_declare(queue=self.task_queue, durable=True)
            channel.basic_publish(
                exchange="",
                routing_key=self.task_queue,
                body=json.dumps(message.to_json()),
                properties=pika.BasicProperties(
                    delivery_mode=2
                )
            )
            logger.info(f"Published message {message.id} to {self.task_queue}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    @staticmethod
    def get_handler() -> callable:
        """Dynamically import and return the handler function for a queue"""
        try:
            handler_path = settings.ECHO_SETTINGS.get('CALLBACK', "echo_client.default_callback.echo_callback")
            module_path, handler_name = handler_path.rsplit('.', 1)
            module = import_module(module_path)
            handler = getattr(module, handler_name)

            if not callable(handler):
                raise ValueError(f"Handler {handler_path} is not callable")

            return handler
        except (ImportError, AttributeError) as e:
            raise ValueError(f"Could not import handler {handler_path}: {str(e)}")

    def start_consuming(self):
        """Start consuming messages from a queue"""

        callback = self.get_handler()

        def wrapped_callback(ch, method, properties, body):
            try:
                message = json.loads(body)
                logger.info(f"Received message from {self.confirmation_queue}")
                msg = MessageFactory.parse(message)
                callback(msg)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received: {body}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        channel = self.connect()
        channel.queue_declare(queue=self.confirmation_queue, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=self.confirmation_queue,
            on_message_callback=wrapped_callback
        )

        logger.info(f"Starting consumer for queue {self.confirmation_queue}")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
        except Exception as e:
            logger.error(f"Consumer error: {e}")
            raise
        finally:
            self.close()

    def close(self):
        """Close the connection"""
        if self._connection and self._connection.is_open:
            self._connection.close()
            self._connection = None
            self._channel = None
            logger.info("RabbitMQ connection closed")