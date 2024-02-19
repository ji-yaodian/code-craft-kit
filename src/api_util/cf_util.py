"""
模块描述

Authors: jiyaodian
Date:    2023/6/2
"""
import os

import httpx

g_cf_host = os.getenv('CF_HOST', "xxxx.com")
g_user = os.getenv('CF_USER', "xxx")
g_password = os.getenv('CF_PASSWORD', "yyy")

g_auth = (g_user, g_password)
headers = {
    "Accept": "application/json"
}


def get_content(cf_id, auth=g_auth, host=g_cf_host):
    url = f"{host}/confluence/rest/api/content/{cf_id}?expand=body.storage,version,space"
    ret = httpx.get(url, auth=auth, follow_redirects=True, timeout=3)
    return ret.json()


def list_children_pages(cf_id, auth=g_auth, host=g_cf_host, limit=1000):
    """
    获取子页面
    :param cf_id:
    :param auth:
    :param host:
    :return:
    """
    url = f"{host}/confluence/rest/api/content/{cf_id}/child/page?limit={limit}"
    ret = httpx.get(url, auth=auth, follow_redirects=True, timeout=3, headers=headers)
    return ret.json()['results']


def create_content(title, body, parent_id, auth=g_auth, host=g_cf_host):
    url = f"{host}/confluence/rest/api/content"
    parent_page = get_content(parent_id)
    data = {
        "type": "page",
        "title": title,
        "ancestors": [{"id": parent_id}],
        "space": {
            "id": parent_page['space']['id'],
            "name": parent_page['space']['name'],
        },
        "body": {
            "storage": {
                "value": body,
            }
        }
    }
    ret = httpx.post(url, headers=headers, auth=auth, json=data, follow_redirects=True)
    return ret.json()


def append_content(cf_id, body: str, auth=g_auth, host=g_cf_host):
    doc = get_content(cf_id)
    url = f"{host}/confluence/rest/api/content/{cf_id}"
    doc['body']['storage']['value'] += body
    doc['version']['number'] += 1
    ret = httpx.put(url, headers={'Content-Type': "application/json"}, auth=auth, json=doc, follow_redirects=True)
    return ret.json()


if __name__ == '__main__':
    append_body = 'test'
    print(append_content('292913445', append_body))
