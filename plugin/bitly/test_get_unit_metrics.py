from .get_unit_metrics import get_unit_metrics


def test_returns_rounded_day():
    metrics = get_unit_metrics(
        {
            "unit_reference": "2023-11-17T12:19:20+0000",
            "metrics": [{"value": "US", "clicks": 4}, {"value": "GB", "clicks": 2}],
            "units": 1,
            "unit": "day",
            "facet": "countries",
        },
        "link/linkid",
    )
    assert metrics == [
        {
            "link_id": "link/linkid",
            "timestamp": "2023-11-17T00:00:00+0000",
            "country": "US",
            "clicks": 4,
        },
        {
            "link_id": "link/linkid",
            "timestamp": "2023-11-17T00:00:00+0000",
            "country": "GB",
            "clicks": 2,
        },
    ]


def test_returns_rounded_hour():
    metrics = get_unit_metrics({
        "unit_reference": "2023-11-17T12:19:20+0000",
        "metrics": [
            {
                "value": "US",
                "clicks": 4
            },
            {
                "value": "GB",
                "clicks": 2
            }
        ],
        "units": 1,
        "unit": "hour",
        "facet": "countries"
    }, "link/linkid")
    assert metrics == [{
            "link_id": "link/linkid",
            "timestamp": "2023-11-17T12:00:00+0000",
            "country": "US",
            "clicks": 4
        },
        {
            "link_id": "link/linkid",
            "timestamp": "2023-11-17T12:00:00+0000",
            "country": "GB",
            "clicks": 2
        }
    ]

def test_returns_rounded_month():
    metrics = get_unit_metrics({
        "unit_reference": "2023-11-17T12:19:20+0000",
        "metrics": [
            {
                "value": "US",
                "clicks": 4
            },
            {
                "value": "GB",
                "clicks": 2
            }
        ],
        "units": 1,
        "unit": "month",
        "facet": "countries"
    }, "link/linkid")
    assert metrics == [{
            "link_id": "link/linkid",
            "timestamp": "2023-11-01T00:00:00+0000",
            "country": "US",
            "clicks": 4
        },
        {
            "link_id": "link/linkid",
            "timestamp": "2023-11-01T00:00:00+0000",
            "country": "GB",
            "clicks": 2
        }
    ]

def test_returns_rounded_week():
    metrics = get_unit_metrics({
        "unit_reference": "2023-11-17T12:19:20+0000",
        "metrics": [
            {
                "value": "US",
                "clicks": 4
            },
            {
                "value": "GB",
                "clicks": 2
            }
        ],
        "units": 1,
        "unit": "week",
        "facet": "countries"
    }, "link/linkid")
    assert metrics == [{
            "link_id": "link/linkid",
            "timestamp": "2023-11-13T00:00:00+0000",
            "country": "US",
            "clicks": 4
        },
        {
            "link_id": "link/linkid",
            "timestamp": "2023-11-13T00:00:00+0000",
            "country": "GB",
            "clicks": 2
        }
    ]
