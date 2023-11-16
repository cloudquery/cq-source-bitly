from typing import Generator, Dict, Any
import requests
from .extract_utm import extract_utm

class BitlyClient:
    def __init__(self, api_token, group_id, base_url, extract_utm):
        self._api_token = api_token
        self._group_id = group_id
        self._base_url = base_url
        self._extract_utm = extract_utm

    def _get(self, path, params=None):
        url = self._base_url + path
        headers = {"Authorization": f"Bearer {self._api_token}"}
        return requests.get(url, headers=headers, params=params)

    def list_bitlinks(self, search_after=""):
        resp = self._get("groups/" + self._group_id + "/bitlinks", {"size": 50, "search_after": search_after})
        if resp.status_code != 200:
            raise Exception(f"Failed to list bitlinks: {resp.text}")
        
        resp = resp.json()
        for link in resp["links"]:
            if not self._extract_utm or "long_url" not in link.keys():
                yield link
            utm_tags = extract_utm(link["long_url"])
            yield link | utm_tags
        if resp["pagination"]["search_after"]:
            yield from self.list_bitlinks(resp["pagination"]["search_after"])

    # def list_forms(self, page=1):
    #     params = {"page": page, "page_size": 200}
    #     resp = self._get("/forms", params=params)
    #     if resp.status_code != 200:
    #         raise Exception(f"Failed to list forms: {resp.text}")

    #     resp = resp.json()
    #     for form in resp["items"]:
    #         yield form

    #     if resp["page_count"] > page:
    #         yield from self.list_forms(page + 1)

    # def list_form_responses(self, form_id, page=1):
    #     params = {"page": page, "page_size": 1000}
    #     resp = self._get(f"/forms/{form_id}/responses", params=params)
    #     if resp.status_code != 200:
    #         raise Exception(f"Failed to list form responses: {resp.text}")

    #     resp = resp.json()
    #     for form in resp["items"]:
    #         yield form

    #     if resp["page_count"] > page:
    #         yield from self.list_form_responses(page + 1)
