# Native Import
from time import time
import logging

# Third party imports
from requests import Session
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)

class MAV4:

    def __init__(self, username=None, password=None, host="https://api.intelligence.fireeye.com"):
        self.username = username
        self.password = password
        self.host = host
        self._session = Session()
        data_token = self._auth()
        logger.debug(data_token)
        self.token_expiration_time = time() + data_token["expires_in"]
        self.token = "Bearer %s" % data_token["access_token"]

    def _auth(self):
        """
        Returns an access token.
        """
        auth = HTTPBasicAuth(self.username, self.password)
        url = "%s/token" % self.host
        data = { "grant_type": "client_credentials" }
        headers = { "content-type": "application/x-www-form-urlencoded" }
        return self._session.post(url=url, data=data, headers=headers, auth=auth).json()

    def _retrieve(self, item_type, start=None, end=None, limit=25, value=None, next_pointer=None):
        url = "%s/v4/%s" % (self.host, item_type)
        headers = {
            "Authorization": self.token,
            "accept": "application/json",
            "X-App-Name": "cybercti client",
        }
        if next_pointer is not None:
            params = { "next": str(next_pointer) }
        else:
            params = {
                "limit": limit,
            }
            if start: # Supported by vuln, indicators and reports
                params["start_epoch"] = start.strftime('%s')
            if end: # Supported by vuln, indicators and reports
                params["end_epoch"] = end.strftime('%s')
            if value: # Supported by indicator
                params["value"] = value
        response = self._session.get(url=url, headers=headers, params=params)
        return response

    def get_items(self, item_type, start=None, end=None, limit=25, value=None, next_pointer=None):
        response = self._retrieve(item_type, start, end, limit, value, next_pointer)
        if response.status_code == 200:
            data = response.json()
        elif response.status_code == 204:
            data = None
        else:
            logger.error("Error Code of %s with message of %s " % (response.status_code, response.text))
            raise RuntimeError(response.text)
        return data

    def search(self, query, item_type=None, limit=25, next_pointer=None):
        url = "%s/v4/search" % (self.host)
        headers = {
            "Authorization": self.token,
            "accept": "application/json",
            "X-App-Name": "cybercti client",
            "content-type": "application/json",
        }
        data = {
            "limit": limit,
            "search": query,
        }
        if next_pointer:
            data["next"] = str(next_pointer)
        if item_type: # Currently undocumented parameter, filter results by: threat-actor malware vulnerability indicator report
            data["type"] = item_type
        response = self._session.post(url=url, headers=headers, json=data)
        return response.json()

    def get_detail(self, item_type, id):
        url = "%s/v4/%s/%s" % (self.host, item_type, id)
        headers = {
            "Authorization": self.token,
            "accept": "application/json",
            "X-App-Name": "cybercti client",
            "content-type": "application/json",
        }
        response = self._session.get(url=url, headers=headers)
        return response.json()
