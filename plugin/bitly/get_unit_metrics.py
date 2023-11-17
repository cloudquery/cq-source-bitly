from datetime import datetime, timedelta


def get_start_date(unit_reference: str, unit: str) -> str:
    match unit:
        case "day":
            return (
                datetime.strptime(unit_reference, "%Y-%m-%dT%H:%M:%S%z")
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .strftime("%Y-%m-%dT%H:%M:%S%z")
            )
        case "hour":
            return (
                datetime.strptime(unit_reference, "%Y-%m-%dT%H:%M:%S%z")
                .replace(minute=0, second=0, microsecond=0)
                .strftime("%Y-%m-%dT%H:%M:%S%z")
            )
        case "month":
            return (
                datetime.strptime(unit_reference, "%Y-%m-%dT%H:%M:%S%z")
                .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                .strftime("%Y-%m-%dT%H:%M:%S%z")
            )
        case "week":
            dt_object = datetime.strptime(unit_reference, "%Y-%m-%dT%H:%M:%S%z")
            days_to_subtract = dt_object.weekday()
            start_of_week = dt_object - timedelta(days=days_to_subtract)
            return start_of_week.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S%z")

        case _:
            raise ValueError(f"Invalid unit: {unit}")


def get_unit_metrics(data: dict, link_id: str, value_key: str):
    start_date = get_start_date(data["unit_reference"], data["unit"])
    return list(
        map(
            lambda metric: {
                "link_id": link_id,
                "timestamp": start_date,
                value_key: metric["value"],
                "clicks": metric["clicks"],
                "unit": data["unit"],
            },
            data["metrics"],
        )
    )
