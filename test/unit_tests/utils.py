import json


def check_against_expected(lens, expected):
    result = lens.to_json()
    assert json.loads(json.dumps(result)) == json.loads(expected)