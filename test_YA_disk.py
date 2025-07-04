import pytest
import requests
import json
import uuid

BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
TOKEN_YA = "Token"
HEADERS = {
    "Authorization": f"OAuth {TOKEN_YA}",
    "Content-Type": "application/json"
}

def create_folder(folder_name):
    params = {"path": folder_name}
    response = requests.put(BASE_URL, headers=HEADERS, params=params)
    return response

def test_create_folder():
    folder_name = f"test_folder_{uuid.uuid4().hex}"
    response = create_folder(folder_name)
    assert response.status_code == 201
    check_response = requests.get(BASE_URL, headers=HEADERS, params={"path": folder_name})
    assert check_response.status_code == 200
    requests.delete(BASE_URL, headers=HEADERS, params={"path": folder_name})

def test_create_folder_already_exists():
    folder_name = f"test_folder_{uuid.uuid4().hex}"
    create_folder(folder_name)
    response = create_folder(folder_name)
    assert response.status_code == 409
    assert "error" in response.json()
    assert response.json()["error"] == "Ошибка. Папка уже существует"
    requests.delete(BASE_URL, headers=HEADERS, params={"path": folder_name})


def test_create_folder_no_authorization():
    folder_name = f"test_folder_{uuid.uuid4().hex}"
    response = requests.put(
        BASE_URL,
        headers={"Authorization": "OAuth invalid_token"},
        params={"path": folder_name}
    )

    assert response.status_code == 401
    assert "error" in response.json()
    assert response.json()["error"] == "Ошибка. Вы не авторизованы"


def test_create_folder_invalid_name():
    invalid_folder_names = [
        "",
        "   ",
        "folder\\name",
        "folder/name",
    ]

    for folder_name in invalid_folder_names:
        response = create_folder(folder_name)
        assert response.status_code == 400
        assert "error" in response.json()


def test_create_folder_no_token():
    folder_name = f"test_folder_{uuid.uuid4().hex}"
    response = requests.put(
        BASE_URL,
        headers={"Content-Type": "application/json"},
        params={"path": folder_name}
    )

    assert response.status_code == 401
    assert "error" in response.json()
    assert response.json()["error"] == "Ошибка. Вы не авторизованы"