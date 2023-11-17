from typing import Any, Generator

import pyarrow as pa
from cloudquery.sdk.scheduler import TableResolver
from cloudquery.sdk.schema import Column
from cloudquery.sdk.schema import Table
from cloudquery.sdk.schema.resource import Resource
from cloudquery.sdk.types import JSONType
from plugin.bitly.get_unit_metrics import get_unit_metrics

from plugin.client import Client


class BitlinksClicksCountries(Table):
    def __init__(self, countries_summary_unit) -> None:
        self._countries_summary_unit = countries_summary_unit
        super().__init__(
            name="bitlinks_clicks_countries",
            title="Bitlinks Clicks by Country",
            is_incremental=True,
            columns=[
                Column("link_id", pa.string()),
                Column("timestamp", pa.timestamp(unit="s")),
                Column("country", pa.string()),
                Column("clicks", pa.int64()),
            ],
        )

    @property
    def resolver(self):
        return BitlinksClicksCountriesResolver(table=self, countries_summary_unit=self._countries_summary_unit)


class BitlinksClicksCountriesResolver(TableResolver):
    def __init__(self, table, countries_summary_unit) -> None:
        self._countries_summary_unit = countries_summary_unit
        super().__init__(table=table)

    def resolve(
        self, client: Client, parent_resource: Resource
    ) -> Generator[Any, None, None]:
        link_stats = client.client.get_link_countries_clicks(parent_resource.item["id"], self._countries_summary_unit)
        metrics = get_unit_metrics(link_stats, parent_resource.item["id"])
        return metrics
