from collections.abc import Generator

from fastapi import status
from fastapi.testclient import TestClient
from pytest import fixture

from src.main import app


@fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client


def test_read_file(client: TestClient):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.template, response.text


def test_upload_file(client: TestClient):
    file_name = "test_imaginary_file.csv"
    file_content = "imaginary file content test_upload_file"
    files = {"file": (file_name, file_content, "text/plain")}
    response = client.post("/", files=files)

    assert response.status_code == status.HTTP_200_OK, response.text
