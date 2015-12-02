
class InventoryModel(object):
    """
    Security Model saves JSON data to an elastic database.
    """

    def __init__(self, es):
        """ Requires an elastic search object for saving to database.
        Args:
          es (ElasticSearch): instance of elastic db
        """
        self.es = es

    def save(self, data):
        """ Saves data to elastic search
        Uses the host name as the index for elastic search.
        This hostname should have been whitelisted before getting here!

        Args:
          data (dict): dictionary of json data
            example:
        """
        self.es.index(index='inventory', doc_type='server', body=data)
