# Bitly Source Plugin for CloudQuery

Bitly plugin for CloudQuery to get links and their stats.

## Spec

```yaml
kind: source
spec:
  name: "bitly"
  registry: "docker"
  path: "docker.cloudquery.io/cloudquery/source-bitly:v1.0.0"
  tables: ['*']
  destinations: ["sqlite"]
  spec:
    group_id: ${BITLY_GROUP_ID}     # mandatory
    api_token: ${BITLY_API_TOKEN}   # mandatory
    extract_utm: true               # optional. If set, extracts utm_tags from the long_url into separate columns
    # optional. unit to use to query last 1 {unit} of clicks by a country. Default: month. Values: hour, day, week, month.
    countries_summary_unit: "month" 
    # optional. unit to use to query last 1 {unit} of clicks by a referrer. Default: month. Values: hour, day, week, month.
    referrers_summary_unit: "month" 
    #optional: get data only for the links on the list 
    only: 
      - bit.ly/1234567
    # optional, includes only links created after the specified date. Supported formats:
    # - "YYYY-MM-DD"
    # - "-<number> <unit>" where number is integer and unit is "day", "week"
    created_after: "-1 day"
```

## Tables

### Bitlinks

[Source API](https://dev.bitly.com/api-reference/#getBitlinksByGroup)

|Column name | Type |
|---|---|
| _cq_sync_time| timestamp |
| _cq_source_name| string |
|created_at | timestamp |
|id | string, primary key|
|link | string|
|custom_bitlinks |JSON|
|launchpad_ids |JSON|
|campaign_ids |JSON|
|long_url | string|
|title | string|
|archived | boolean|
|created_by | string|
|client_id | string|
|tags |JSON|
|deeplinks |JSON|
|references |JSON|

With `extract_utm` set to `true`, the following columns are also added:

|Column name | Type |
|---|---|
| _cq_sync_time| timestamp |
| _cq_source_name| string |
|utm_source | string |
|utm_medium | string |
|utm_campaign | string |
|utm_id | string |
|utm_term | string |
|utm_content | string |

### Bitlinks Clicks

[Source API](https://dev.bitly.com/api-reference/#getClicksForBitlink)

This table is incremental and adds daily stats.

|Column name | Type |
|---|---|
| _cq_sync_time| timestamp |
| _cq_source_name| string |
| link_id | string |
| date | timestamp |
| clicks | int64 |

### Bitlinks Click Summary

[Source API](https://dev.bitly.com/api-reference/#getClicksSummaryForBitlink)

Gets a 45 day summary of link clicks.

|Column name | Type |
|---|---|
| _cq_sync_time| timestamp |
| _cq_source_name| string |
| link_id | string, primary key|
| unit_reference | timestamp |
| total_clicks | int64 |
| units | int16 |
| unit | string |

### Bitlinks Clicks Countries

[Source API](https://dev.bitly.com/api-reference/#getMetricsForBitlinkByCountries)

This table is incremental and adds stats based on the configured value of `countries_summary_unit`.

Each sync adds rows (if not present already) for the last 1 {`countries_summary_unit`}.

|Column name | Type |
|---|---|
| _cq_sync_time| timestamp |
| _cq_source_name| string |
| link_id | string |
| timestamp | timestamp |
| country | string |
| clicks | int64 |
| unit | string |

### Bitlinks Clicks Referrers

[Source API](https://dev.bitly.com/api-reference/#getMetricsForBitlinkByReferrers)

This table is incremental and adds stats based on the configured value of `referrers_summary_unit`.

Each sync adds rows (if not present already) for the last 1 {`referrers_summary_unit`}.

|Column name | Type |
|---|---|
| _cq_sync_time| timestamp |
| _cq_source_name| string |
| link_id | string |
| timestamp | timestamp |
| referrer | string |
| clicks | int64 |
| unit | string |
