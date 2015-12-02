import logging
import falcon
import settings


def cross_domain(req, resp):
    """ Middleware for handling Cross Domain requests.
    Only allow from the whitelist in settings.ALLOWED_HTTP_ORIGIN_DOMAINS.
    If it is there, send back the same HTTP_ORIGIN as Access-Control-Allow-Origin.
    Otherwise, use default domain.
    Raises:
      falcon.HTTPError: if users is not a known domain. HTTP Status: 400

    """
    if 'HTTP_ORIGIN' in req.env:
        if req.env['HTTP_ORIGIN'] in settings.ALLOWED_HTTP_ORIGIN_DOMAINS:
            return resp.set_header('Access-Control-Allow-Origin', req.env['HTTP_ORIGIN'])
        logging.warn('Unknown Cross Domain Attempt from: %s' % req.env['HTTP_ORIGIN'])
        resp.set_header('Access-Control-Allow-Origin', settings.DEFAULT_ORIGIN_URL)
        raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'Origin not recognized: %s' % req.env['HTTP_ORIGIN'])