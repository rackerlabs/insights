"""
The following variables always mean the same things in the following code:
    @param tenant_id: {string} A rackspace tenant id.
        e.g. 123456
    @param auth_token: {string} A valid rackspace auth token for this tenant
        e.g. ABCDeasfasf2ar32...
    @param agent_id: {string} Monitoring agent id of the server we want to hit
        e.g. ABCDe24-123d-3225-af2-34twfetr3
    @param host_info_types: {string} CSV of the host info types we want
        e.g. magento || nginx_config,magento,wordpress
"""

import requests
import logging
LOG = logging.getLogger(__name__)

monitoring_api_url = 'https://monitoring.api.rackspacecloud.com/v1.0/%s'


def get_agent_host_info(tenant_id, auth_token, agent_id, host_info_types):
    """Function to get hostinfo data from a rackspace monitoring agent

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
    """Function to get all available hostinfo types from a rackspace
    monitoring agent

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


def host_info_to_json(host_info_data):
    """Given the raw hostinfo data this will rip out the
    info parts of the hostinfos and discard the timestamps
    and errors
    e.g.
      "x" = {"info": [{validJson}], "timestamp": 12235, "error": "string"}
    to
      "x" = [{validJson}]
    This merely returns validJson, you can get a json string with
      json.dumps
    which you can then load back in with
      json.loads
    """

    host_info_infos = {}
    for key in host_info_data:
        host_info_infos[key] = host_info_data[key]['info']
    return host_info_infos


def get_all_host_info(tenant_id, auth_token, agent_id):
    """Function to get all hostinfo data from an agent
    The returned data will contain timestamps, and errors as well

    @return {dict} e.g. {"x" = {"info": [{validJson}], 
                                "timestamp": 12235,
                                 "error": "string"}}
    """
    host_info_types = get_agent_host_info_types(
        tenant_id, auth_token, agent_id)
    host_info_types_string = ",".join(host_info_types)
    host_info_data_raw = get_agent_host_info(
        tenant_id, auth_token, agent_id, host_info_types_string)
    return host_info_data_raw


def get_all_host_info_data(tenant_id, auth_token, agent_id):
    """Function to return hostinfo data stripped of timestamp and error data"""
    host_info_data_raw = get_all_host_info(tenant_id, auth_token, agent_id)
    host_info_data_stripped = host_info_to_json(host_info_data_raw)
    return host_info_data_stripped
