from typing import Any, Generator

import pyarrow as pa
from cloudquery.sdk.scheduler import TableResolver
from cloudquery.sdk.schema import Column
from cloudquery.sdk.schema import Table
from cloudquery.sdk.schema.resource import Resource
from cloudquery.sdk.types import JSONType

from plugin.client import Client


class BitlinksClicks(Table):
    def __init__(self) -> None:
        super().__init__(
            name="bitlinks_clicks",
            title="Bitlinks Clicks",
            is_incremental=True,
            columns=[
                Column("link_id", pa.string()),
                Column("date", pa.timestamp(unit="s")),
                Column("clicks", pa.int64()),
            ],
        )

    @property
    def resolver(self):
        return BitlinksClicksResolver(table=self)


class BitlinksClicksResolver(TableResolver):
    def __init__(self, table) -> None:
        super().__init__(table=table)

    def resolve(
        self, client: Client, parent_resource: Resource
    ) -> Generator[Any, None, None]:
        link_stats = client.client.get_link_clicks(parent_resource.item["id"])
        return list(
            map(
                lambda x: {
                    "link_id": parent_resource.item["id"],
                    "date": x["date"],
                    "clicks": x["clicks"],
                },
                link_stats,
            )
        )
