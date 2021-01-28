import requests

def _url(harmony_host_url: str, uri: str) -> str:
    return f'{harmony_host_url}/{uri}'


def find_by_attr(items: list, attr: str, val: str) -> str:
    for i in items:
        if i[attr] == val:
            return i


def api(harmony_host_url: str, uri: str):
    return requests.get(_url(harmony_host_url, uri)).json()
