from urllib.parse import urlparse
from urllib.parse import parse_qs


def extract_utm(url: str) -> dict:
    # extract utm tags from the input url
    parsed_url = urlparse(url)
    query_string = parse_qs(parsed_url.query)
    result = dict()
    for x in query_string.keys():
        result[x] = query_string[x][0]

    return result
