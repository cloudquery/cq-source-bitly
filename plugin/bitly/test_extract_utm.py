from .extract_utm import extract_utm

def test_returns_empty_dict():
    result = extract_utm("https://www.cloudquery.io/blog/announcing-cloudquery-new-hub")
    assert(result == {})

def test_extracts_source():
    result = extract_utm("https://www.cloudquery.io/blog/announcing-cloudquery-new-hub?utm_source=youtube")
    assert(result["utm_source"] == "youtube")

def test_extracts_medium():
    result = extract_utm("https://www.cloudquery.io/blog/announcing-cloudquery-new-hub?utm_medium=video")
    assert(result["utm_medium"] == "video")


def test_extracts_campaign():
    result = extract_utm("https://www.cloudquery.io/blog/announcing-cloudquery-new-hub?utm_campaign=spring_sale")
    assert(result["utm_campaign"] == "spring_sale")

def test_extracts_id():
    result = extract_utm("https://www.cloudquery.io/blog/announcing-cloudquery-new-hub?utm_id=cid")
    assert(result["utm_id"] == "cid")

def test_extracts_term():
    result = extract_utm("https://www.cloudquery.io/blog/announcing-cloudquery-new-hub?utm_term=paid_keyword")
    assert(result["utm_term"] == "paid_keyword")

def test_extracts_content():
    result = extract_utm("https://www.cloudquery.io/blog/announcing-cloudquery-new-hub?utm_content=content")
    assert(result["utm_content"] == "content")

def test_extracts_all():
    result = extract_utm("https://cloudquery.io?utm_source=youtube&utm_medium=video&utm_campaign=spring_sale&utm_id=cid&utm_term=paid_keywords&utm_content=content")
    assert(result["utm_source"] == "youtube")
    assert(result["utm_medium"] == "video")
    assert(result["utm_campaign"] == "spring_sale")
    assert(result["utm_id"] == "cid")
    assert(result["utm_term"] == "paid_keywords")
    assert(result["utm_content"] == "content")