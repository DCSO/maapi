# Native Import
import logging
from typing import Dict


# Local Imports
from maapi import MAAPI

logger = logging.getLogger(__name__)

class DTM(MAAPI):
    """
    API client for Mandiant Advantage Digitial Threat Monitoring.
    """

    def __init__(self, *args, **kwargs):
        self.sub_type = 'DTM'
        super().__init__(*args, **kwargs)

    def get_email_settings(self):
        """
        Get the email settings for the organization.
        """
        url = f"{self.host}/v4/dtm/settings/email"
        response = self._http_get(url=url)
        return response.json()

    def get_vocab_openapi(self):
        """
        Get the Open API spec for this REST API
        """
        headers = {
            "accept": "text/yaml"
        }
        url = f"{self.host}/v4/dtm/vocab/openapi"
        response = self._http_get(url=url, headers=headers)
        return response


    def get_monitor(self, monitor_id):
        """
        Get the details of a given monitor_id.
        """
        url = f"{self.host}/v4/dtm/monitors/{monitor_id}"
        response = self._http_get(url=url)
        return response.json()

    def get_monitor_list(self, limit=50):
        """
        Get a list of monitors
        """
        url = f"{self.host}/v4/dtm/monitors"
        params = {
            "size": limit,
        }
        response = self._http_get(url=url, params=params)
        return response.json()

    def _update_monitor_statuses(self, monitor_id, enabled=None, email_notify_enabled=None, email_notify_immediate=None):
        """
        Update one or more of the Monitor Status Fields
        """
        data = {
            "enabled": enabled,
            "email_notify_enabled": email_notify_enabled,
            "email_notify_immediate": email_notify_immediate,
        }
        url = f"{self.host}/v4/dtm/monitors/{monitor_id}"
        response = self._http_patch(url=url, json=data)
        return response.json()

    def enable_monitor(self, monitor_id):
        """
        Enable a Monitor
        """
        return self._update_monitor_statuses(monitor_id, enabled=True)

    def disable_monitor(self, monitor_id):
        """
        Disable a Monitor
        """
        return self._update_monitor_statuses(monitor_id, enabled=False)

    def get_alerts(self, size=25, status=None, life="10m", order="desc", refs="false", sort="created_at", monitor_ids=None):
        """
        Get a list of monitors, optionally filtered by monitor_ids.
        """
        url = f"{self.host}/v4/dtm/alerts"
        params = {
            "size": size,
            "status": status,
            "life": life,
            "order": order,
            "refs": refs,
            "sort": sort,
            "monitor_id": monitor_ids
        }
        response = self._http_get(url=url, params=params)
        return response.json()

    def search_research_tools(self, query, limit=25, doc_types=None, since=None, until=None, truncate=None):
        """
        Search Research Tools
        """
        url = f"{self.host}/v4/dtm/docs/search"
        params = {
            "size": limit,
            "doc_type": doc_types,
            "since": since,
            "until": until,
            "truncate": truncate,
        }
        data = {
            "query": query
        }
        response = self._http_post(url=url, json=data, params=params)
        return response.json()

    def get_document(self, doc_id, doc_type, refs=False, truncate=None, sanitize=True):
        """
        Retrieve document by doc_id and doc_type.
        Options to include the entities and classifiations (refs), optionally truncate the text and sanitize the HTML.
        """
        url = f"{self.host}/v4/dtm/docs/{doc_type}/{doc_id}"
        params = {
            "refs": refs,
            "truncate": truncate,
            "sanitize": sanitize,
        }
        response = self._http_get(url=url, params=params)
        return response.json()

    def get_forum_boards(self, forum_id:int) -> Dict:
        """
        Retrieve a list of Boards for a given forum_id
        """
        url = f"{self.host}/v4/dtm/views/forums/{forum_id}"
        response = self._http_get(url=url)
        return response.json()

    def get_forum_boards_threads(self, forum_id:int, board_name:int) -> Dict:
        """
        Retrieve a list of Threads for a given forum_id and board_name
        """
        url = f"{self.host}/v4/dtm/views/forums/{forum_id}/boards"
        params = {
            "board": board_name
        }
        response = self._http_get(url=url, params=params)
        return response.json()
