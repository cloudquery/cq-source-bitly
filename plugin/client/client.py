from dataclasses import dataclass, field
from cloudquery.sdk.scheduler import Client as ClientABC

from plugin.bitly.client import BitlyClient

DEFAULT_CONCURRENCY = 100
DEFAULT_QUEUE_SIZE = 10000


@dataclass
class Spec:
    api_token: str
    group_id: str
    base_url: str = field(default="https://api-ssl.bitly.com/v4/")
    concurrency: int = field(default=DEFAULT_CONCURRENCY)
    queue_size: int = field(default=DEFAULT_QUEUE_SIZE)
    extract_utm: bool = field(default=False)
    countries_summary_unit: str = field(default="month")
    referrers_summary_unit: str = field(default="month")
    only: list[str] = field(default_factory=list)

    def validate_summary_unit(self, unit: str, name: str):
        if unit not in ["hour", "day", "week", "month"]:
            raise Exception(f"{name} must be one of hour, day, week, month")

    def validate(self):
        if self.api_token is None:
            raise Exception("api_token must be provided")
        if self.group_id is None:
            raise Exception("group_id must be provided")
        self.validate_summary_unit(
            self.countries_summary_unit, "countries_summary_unit"
        )
        self.validate_summary_unit(
            self.referrers_summary_unit, "referrers_summary_unit"
        )


class Client(ClientABC):
    def __init__(self, spec: Spec) -> None:
        self._spec = spec
        self._client = BitlyClient(
            spec.api_token,
            spec.group_id,
            spec.base_url,
            spec.extract_utm,
            spec.countries_summary_unit,
            spec.referrers_summary_unit,
        )

    def id(self):
        return "bitly"

    @property
    def client(self) -> BitlyClient:
        return self._client
