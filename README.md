# Bitly Source Plugin for CloudQuery

Bitly plugin for CloudQuery to get links and their stats.

## Spec

```yaml
kind: source
spec:
  name: "bitly"
  registry: "grpc"
  path: "localhost:7777"
  tables: ['*']
  destinations: ["sqlite"]
  spec:
    group_id: ${BITLY_GROUP_ID}     # mandatory
    api_token: ${BITLY_API_TOKEN}   # mandatory
    extract_utm: true               # optional. If set, extracts utm_tags from the long_url into separate columns
```

## Tables

### Bitlinks

[Source API](https://dev.bitly.com/api-reference/#getBitlinksByGroup)

|Column name | Type |
|---|---|
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
| link_id | string |
| date | timestamp |
| clicks | int64 |

### Bitlinks Click Summary

[Source API](https://dev.bitly.com/api-reference/#getClicksSummaryForBitlink)

Gets a 45 day summary of link clicks.

|Column name | Type |
|---|---|
| link_id | string, primary key|
| unit_reference | timestamp |
| total_clicks | int64 |
| units | int16 |
| unit | string |
