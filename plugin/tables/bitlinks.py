from typing import Any, Generator

import pyarrow as pa
from cloudquery.sdk.scheduler import TableResolver
from cloudquery.sdk.schema import Column
from cloudquery.sdk.schema import Table
from cloudquery.sdk.schema.resource import Resource
from cloudquery.sdk.types import JSONType
from plugin.client import Client
from .bitlinks_click_summary import BitlinksClickSummary
from .bitlinks_clicks import BitlinksClicks
from .bitlinks_clicks_countries import BitlinksClicksCountries
from .bitlinks_clicks_referrers import BitlinksClicksReferrers


class Bitlinks(Table):
    def __init__(
        self,
        extract_utm=False,
        countries_summary_unit="month",
        referrers_summary_unit="month",
        link_filter=[],
    ) -> None:
        self.link_filter = link_filter
        columns = [
            Column("created_at", pa.timestamp(unit="s")),
            Column("id", pa.string(), primary_key=True),
            Column("link", pa.string()),
            Column("custom_bitlinks", JSONType()),
            Column("launchpad_ids", JSONType()),
            Column("campaign_ids", JSONType()),
            Column("long_url", pa.string()),
            Column("title", pa.string()),
            Column("archived", pa.bool_()),
            Column("created_by", pa.string()),
            Column("client_id", pa.string()),
            Column("tags", JSONType()),
            Column("deeplinks", JSONType()),
            Column("references", JSONType()),
        ]
        utm_columns = [
            Column("utm_source", pa.string()),
            Column("utm_medium", pa.string()),
            Column("utm_campaign", pa.string()),
            Column("utm_id", pa.string()),
            Column("utm_term", pa.string()),
            Column("utm_content", pa.string()),
        ]
        if extract_utm:
            columns.extend(utm_columns)
        super().__init__(
            name="bitlinks",
            title="bitlinks",
            columns=columns,
            relations=[
                BitlinksClickSummary(),
                BitlinksClicks(),
                BitlinksClicksCountries(countries_summary_unit),
                BitlinksClicksReferrers(referrers_summary_unit),
            ],
        )

    @property
    def resolver(self):
        return BitlinksResolver(table=self, link_filter=self.link_filter)


class BitlinksResolver(TableResolver):
    def __init__(self, table=None, link_filter = []) -> None:
        super().__init__(table=table)
        self.link_filter = link_filter

    def resolve(self, client: Client, parent_resource) -> Generator[Any, None, None]:
        for bitlink in filter(lambda l: len(self.link_filter) == 0 or l["id"] in self.link_filter, client.client.list_bitlinks()):
            yield bitlink

    @property
    def child_resolvers(self):
        return [table.resolver for table in self._table.relations]
