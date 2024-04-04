from typing import Generator, Dict, Any
import requests
from .extract_utm import extract_utm


class BitlyClient:
    def __init__(
        self,
        api_token,
        group_id,
        base_url,
        extract_utm,
        countries_summary_unit,
        referrers_summary_unit,
    ):
        self._api_token = api_token
        self._group_id = group_id
        self._base_url = base_url
        self._extract_utm = extract_utm
        self._countries_summary_unit = countries_summary_unit
        self._referrers_summary_unit = referrers_summary_unit

    def _get(self, path, params=None):
        url = self._base_url + path
        headers = {"Authorization": f"Bearer {self._api_token}"}
        return requests.get(url, headers=headers, params=params)

    def list_bitlinks(self, search_after="", created_after=""):
        resp = self._get(
            f"groups/{self._group_id}/bitlinks",
            {"size": 50, "search_after": search_after, "created_after": created_after},
        )
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

    def get_clicks_summary(self, link_id: str):
        resp = self._get(f"bitlinks/{link_id}/clicks/summary")
        if resp.status_code != 200:
            raise Exception(
                f"Failed to get bitlink clicks summary for link id '{link_id}': {resp.text}"
            )
        yield resp.json()

    def get_link_clicks(self, link_id: str):
        resp = self._get(f"bitlinks/{link_id}/clicks?unit=day&units=45")
        if resp.status_code != 200:
            raise Exception(
                f"Failed to get bitlink clicks summary for link id '{link_id}': {resp.text}"
            )
        return resp.json()["link_clicks"]

    def get_link_countries_clicks(self, link_id: str, unit: str):
        resp = self._get(f"bitlinks/{link_id}/countries?unit={unit}&units=1")
        if resp.status_code != 200:
            raise Exception(
                f"Failed to get bitlink clicks countries for link id '{link_id}': {resp.text}"
            )
        return resp.json()

    def get_link_referrers_clicks(self, link_id: str, unit: str):
        resp = self._get(f"bitlinks/{link_id}/referrers?unit={unit}&units=1")
        if resp.status_code != 200:
            raise Exception(
                f"Failed to get bitlink clicks referrers for link id '{link_id}': {resp.text}"
            )
        return resp.json()
