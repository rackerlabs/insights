from datetime import datetime
import logging
import jsonschema
from schemas import inventory as inventory_schema
from helpers import log_failed_data


class RequestHandler(object):
    """
    Request Handler performs modifications and validations of the users request
    """

    def __init__(self):
        pass

    def is_valid(self, req, data):
        """
        Args:
          req (WSGIRequest): Request from Resource
          data (dict): Dict that represents the json sent via the request
        Returns:
          bool: True if passes json schema and IP validation
        """
        valid = False
        try:
            #jsonschema.validate(data, inventory_schema)
            valid = True
        except:
            file_name = 'failures/%s.log' % datetime.now()
            logging.info('Failed validation see file "%s"' % file_name)
            log_failed_data(file_name, data)

        return valid

    def prepare(self, data, req):
        """ Adds TBD

        Args:
          data (dict): JSON request from the client. Assumed to be validated
          req (WSGIRequest): Falcon request object
        Returns:
          data (dict): JSON for database
        """
        data['timestamp'] = self.get_timestamp()
        return data

    def get_timestamp(self):
        """ Return time stamp"""
        return datetime.now()