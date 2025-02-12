import json

import requests
import requests.cookies

BASE_URL = 'http://localhost:8069/bosmobosmo/'  # match with controller path
LOGIN = ""
PASSWORD = ""
DB = ""
headers = {'Content-type': 'application/json'}


def auth() -> requests.cookies.RequestsCookieJar:
    res = requests.post(
        f'{BASE_URL}auth',
        data=json.dumps({'params': {
            'login': LOGIN,
            'password': PASSWORD,
            'db': DB
        }}),
        headers=headers
    )
    return res.cookies


def list_item(
    cookies: requests.cookies.RequestsCookieJar,
    params: dict[str, object] = {},
    item='materials',
) -> requests.Response:
    res = requests.get(
        f"{BASE_URL}list-{item}",
        params=params,
        cookies=cookies
    )
    return res


def delete_material(
    cookies: requests.cookies.RequestsCookieJar,
    id: int
) -> requests.Response:
    res = requests.get(
        f"{BASE_URL}delete-material",
        params={'id': id},
        cookies=cookies
    )
    return res


def get_material(
    cookies: requests.cookies.RequestsCookieJar,
    id: int
) -> requests.Response:
    res = requests.get(
        f"{BASE_URL}get-material",
        params={'id': id},
        cookies=cookies
    )
    return res


def create_material(
    cookies: requests.cookies.RequestsCookieJar,
    params: dict[str, object]
) -> requests.Response:
    res = requests.post(
        f"{BASE_URL}create-material",
        params=params,
        cookies=cookies
    )
    return res


def update_material(
    cookies: requests.cookies.RequestsCookieJar,
    params: dict[str, object]
) -> requests.Response:
    res = requests.post(
        f"{BASE_URL}update-material",
        params=params,
        cookies=cookies
    )
    return res


if __name__ == "__main__":
    cookies = auth()

    # reset db
    list_material_result = list_item(cookies)
    materials = list_material_result.json()
    list_material_result.raise_for_status()
    for material in materials:
        if material['name'] == 'Spandex':
            delete_material(cookies, material['id'])

    create_result = create_material(
        cookies,
        params={
            'name': 'Spandex',
            'buy_price': 500,
            'supplier_id': 1,
            'code': 5409,
            'type': 'jeans'
        }
    )
    assert create_result.status_code == 200
    assert create_material(
        cookies,
        params={
            'name': 'Spandex',
            'buy_price': 500,
            'supplier_id': 1,
            'code': 5410,
            'type': 'cotton'
        }
    ).status_code == 200

    # Check material creation is succesful
    list_material_result = list_item(cookies)
    list_material_result.raise_for_status()
    materials = list_material_result.json()
    assert 'Spandex' in [material['name'] for material in materials]
    for material in materials:
        if material['name'] == 'Spandex':
            created_material_id = material['id']

    # Test material type filter
    jeans_list = list_item(cookies, {'type': 'jeans'})
    jeans_list.raise_for_status()
    jeans = jeans_list.json()
    assert len(jeans) < len(materials)

    # Test material update
    # Invalid buy price
    update_result = update_material(
        cookies, {'id': created_material_id, 'buy_price': 99}
    )
    assert update_result.status_code == 500
    update_result = update_material(
        cookies, {'id': created_material_id, 'buy_price': 1000}
    )
    assert update_result.status_code == 200
    get_result = get_material(cookies, created_material_id)
    assert get_result.status_code == 200
    assert get_result.json()[0]['buy_price'] == float(1000)
