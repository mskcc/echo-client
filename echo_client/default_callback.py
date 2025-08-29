import logging


logger = logging.getLogger()


def echo_callback(message):
    try:
        print(f"Processing notification: {message}")
        logger.info(f"Processing notification: {message.to_json()}")
    except Exception as e:
        logger.error(f"Error processing notification: {e}")
        raise