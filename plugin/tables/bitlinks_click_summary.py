from typing import Any, Generator

import pyarrow as pa
from cloudquery.sdk.scheduler import TableResolver
from cloudquery.sdk.schema import Column
from cloudquery.sdk.schema import Table
from cloudquery.sdk.schema.resource import Resource
from cloudquery.sdk.types import JSONType

from plugin.client import Client


class BitlinksClickSummary(Table):
    def __init__(self) -> None:
        super().__init__(
            name="bitlinks_click_summary",
            title="Bitlinks Click Summary",
            columns=[
                Column("link_id", pa.string(), primary_key=True),
                Column("unit_reference", pa.timestamp(unit="s")),
                Column("total_clicks", pa.int64()),
                Column("units", pa.int16()),
                Column("unit", pa.string()),
            ],
        )

    @property
    def resolver(self):
        return BitlinksClickSummaryResolver(table=self)


class BitlinksClickSummaryResolver(TableResolver):
    def __init__(self, table) -> None:
        super().__init__(table=table)

    def resolve(
        self, client: Client, parent_resource: Resource
    ) -> Generator[Any, None, None]:
        for link_click_summary in client.client.get_clicks_summary(
            parent_resource.item["id"]
        ):
            link_click_summary["link_id"] = parent_resource.item["id"]
            yield link_click_summary
