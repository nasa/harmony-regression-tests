import requests

ENVIRONMENT_HOSTNAME = {
    'sit': 'harmony.sit.earthdata.nasa.gov',
    'uat': 'harmony.uat.earthdata.nasa.gov',
    'prod': 'harmony.earthdata.nasa.gov'
}


def _harmony_hostname(env: str) -> str:
    return ENVIRONMENT_HOSTNAME[env]


def _url(environment: str, uri: str) -> str:
    return f'https://{_harmony_hostname(environment)}/{uri}'


def find_by_attr(items: list, attr: str, val: str) -> str:
    for i in items:
        if i[attr] == val:
            return i


def api(environment: str, uri: str):
    return requests.get(_url(environment, uri)).json()
