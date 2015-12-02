import logging
import os

ALLOWED_HTTP_ORIGIN_DOMAINS = (
    'http://www.example.com',
)

DEFAULT_ORIGIN_URL = 'https://www.example.com'
LOG_FILE = 'application.log'
LOG_LEVEL = logging.DEBUG
ELASTIC_URL = os.environ['ELASTICSEARCH_PORT_9200_TCP_ADDR']
ELASTIC_PORT = os.environ['ELASTICSEARCH_PORT_9200_TCP_PORT']