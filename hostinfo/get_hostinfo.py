import requests
import logging
LOG = logging.getLogger(__name__)

monitoring_api_url = 'https://monitoring.api.rackspacecloud.com/v1.0/%s'


def get_agent_host_info(tenant_id, auth_token, agent_id, host_info_types):
    """Function to get hostinfo data from a rackspace monitoring agent
    @param tenant_id: {string} A rackspace tenant id.
        e.g. 123456
    @param auth_token: {string} A valid rackspace auth token for this tenant
        e.g. ABCDeasfasf2ar32...
    @param agent_id: {string} Monitoring agent id of the server we want to hit
        e.g. ABCDe24-123d-3225-af2-34twfetr3
    @param host_info_types: {string} CSV of the host info types we want
        e.g. magento || nginx_config,magento,wordpress
    @return {dict} Contains host information returned with keys = types"""

    suffix = ("%s/views/agent_host_info?agentId=%s&include=%s"
              % (tenant_id, agent_id, host_info_types))
    url = (monitoring_api_url % suffix)
    request = requests.get(url, headers={"X-Auth-Token": auth_token})
    if not request.ok:
        msg = ("Agent hostinfo retrieval error. Response code %d. "
               "Response body: %s" % (request.status_code, request.text))
        LOG.error(msg)
        raise Exception(msg)

    try:
        host_info = request.json()['values'][0]['host_info']
    except Exception as exc:
        LOG.error("Unknown error: %s", exc)
    else:
        LOG.debug('Retrieved hostinfo data successfully')
        return host_info


def get_agent_host_info_types(tenant_id, auth_token, agent_id):
    """Function to get hostinfo data from a rackspace monitoring agent
    @param tenant_id: {string} A rackspace tenant id.
        e.g. 123456
    @param auth_token: {string} A valid rackspace auth token for this tenant
        e.g. ABCDeasfasf2ar32...
    @param agent_id: {string} Monitoring agent id of the server we want to hit
        e.g. ABCDe24-123d-3225-af2-34twfetr3
    @return {list} Contains all the supported hostinfos on this agent"""

    suffix = ("%s/agents/%s/host_info_types" % (tenant_id, agent_id))
    url = (monitoring_api_url % suffix)
    request = requests.get(url, headers={"X-Auth-Token": auth_token})
    if not request.ok:
        msg = ("Agent hostinfo types lookup error. Response code %d."
               "Response body: %s" % (request.status_code, request.text))
        LOG.error(msg)
        raise Exception(msg)

    try:
        host_info_types = request.json()['types']
    except Exception as exc:
        LOG.error("Unknown error: %s", exc)
    else:
        LOG.debug('Retrieved a list of possible host info types: %s',
                  host_info_types)
        return host_info_types
