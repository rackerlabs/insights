import logging
import falcon
from inventory.api import InventoryResource
import middleware
import settings

# Start Logging for application
logging.basicConfig(filename=settings.LOG_FILE, level=settings.LOG_LEVEL)

# Temporarily removed
# app = application = falcon.API(after=[middleware.cross_domain])
app = application = falcon.API()
app.add_route('/v1/inventory', InventoryResource())


# This is for local usage
if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server('0.0.0.0', 80, app)
    httpd.serve_forever()