from typing import Any, Generator

import pyarrow as pa
from cloudquery.sdk.scheduler import TableResolver
from cloudquery.sdk.schema import Column
from cloudquery.sdk.schema import Table
from cloudquery.sdk.schema.resource import Resource
from cloudquery.sdk.types import JSONType
from plugin.client import Client

class Bitlinks(Table):
    def __init__(self, extract_utm=False) -> None:
        columns = [
            Column("created_at", pa.timestamp(unit="s")), # todo: change to date
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
            Column("references", JSONType())
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
        )

    @property
    def resolver(self):
        return BitlinksResolver(table=self)


class BitlinksResolver(TableResolver):
    def __init__(self, table=None) -> None:
        super().__init__(table=table)

    def resolve(self, client: Client, parent_resource) -> Generator[Any, None, None]:
        for form in client.client.list_bitlinks():
            yield form

    # @property
    # def child_resolvers(self):
    #     return [table.resolver for table in self._table.relations]

