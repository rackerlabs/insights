import json
import logging
import falcon


def get_json(req):
    """ Helper method to handle converting raw requests into dict for JSON.
    Args:
      req (WSGIRequest): Request
    Returns:
      data (dict): JSON
    Raises:
      falcon.HTTPError: if cannot convert to JSON, sends 400 to user
    """
    try:
        raw_data = req.stream.read()
    except Exception as ex:
        raise falcon.HTTPError(falcon.HTTP_400,
                               'Error',
                               ex.message)
    try:
        data = json.loads(raw_data, encoding='utf-8')
    except Exception:
        raise falcon.HTTPError(falcon.HTTP_400,
                               'Malformed JSON',
                               'Could not decode the request body. The '
                                   'JSON was incorrect.')
    return data


def log_failed_data(filename, data):
    """ Helper method for opening and writing JSON to a log file.
    Used to wrap writes within a try-except block in case server has permission errors.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f)
    except:
        logging.error('cannot save to file "%s"' % filename)