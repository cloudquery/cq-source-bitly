from typing import Any, Generator

import pyarrow as pa
from cloudquery.sdk.scheduler import TableResolver
from cloudquery.sdk.schema import Column
from cloudquery.sdk.schema import Table
from cloudquery.sdk.schema.resource import Resource
from cloudquery.sdk.types import JSONType
from plugin.bitly.get_unit_metrics import get_unit_metrics

from plugin.client import Client


class BitlinksClicksReferrers(Table):
    def __init__(self, referrers_summary_unit) -> None:
        self._referrers_summary_unit = referrers_summary_unit
        super().__init__(
            name="bitlinks_clicks_referrers",
            title="Bitlinks Clicks by Referrer",
            is_incremental=True,
            columns=[
                Column("link_id", pa.string()),
                Column("timestamp", pa.timestamp(unit="s")),
                Column("referrer", pa.string()),
                Column("clicks", pa.int64()),
                Column("unit", pa.string()),
            ],
        )

    @property
    def resolver(self):
        return BitlinksClicksReferrersResolver(
            table=self, referrers_summary_unit=self._referrers_summary_unit
        )


class BitlinksClicksReferrersResolver(TableResolver):
    def __init__(self, table, referrers_summary_unit) -> None:
        self._referrers_summary_unit = referrers_summary_unit
        super().__init__(table=table)

    def resolve(
        self, client: Client, parent_resource: Resource
    ) -> Generator[Any, None, None]:
        link_stats = client.client.get_link_referrers_clicks(
            parent_resource.item["id"], self._referrers_summary_unit
        )
        metrics = get_unit_metrics(link_stats, parent_resource.item["id"], "referrer")
        return metrics
