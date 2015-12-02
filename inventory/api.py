from datetime import datetime
import logging
import falcon
import settings
from models import InventoryModel
from helpers import get_json, log_failed_data
from inventory.utils import RequestHandler
from elasticsearch import Elasticsearch


class InventoryResource(object):

    def __init__(self):
        pass

    def on_post(self, req, resp):
        """ Handle API Posts to /api/inventory
        Uses a request handler to perform data validation and preparation for
        elastic database.

        If any exceptions are raised by the Performance Model during saving. Check the logs.
        Log file is saved based on value of settings.LOG_FILE

        Args:
            req: WSGI Request
            resp: WSGI Response
        Raises:
            falcon.HTTPError: For database level errors
                returns a 202 to the user..this is to prevent a 500 Status
        """
        data = get_json(req)
        handler = RequestHandler()
        if handler.is_valid(req, data):
            data = handler.prepare(data, req)
            # Save Data
            try:
                es = Elasticsearch([settings.ELASTIC_URL], port=settings.ELASTIC_PORT)
                model = InventoryModel(es)
                model.save(data)
            except Exception as e:
                if 'timestamp' in data:
                    data['timestamp'] = str(data['timestamp'])
                file_name = 'failures/%s.log' % datetime.now()
                logging.error('Failed to save to database see file "%s due to %s"' % (file_name, e.message))
                log_failed_data(file_name, data)
                raise falcon.HTTPError(falcon.HTTP_400, 'error', 'saving')

            resp.status = falcon.HTTP_201
            resp.body = '{"title": "created"}'
        else:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'Invalid request')
