import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


@pytest.fixture
def mock_httpx_post():
    with patch("httpx.AsyncClient.post") as mock_post:
        yield mock_post


def test_scan_qr_success(mock_httpx_post):
    # Simulate successful QR code detection and HTTP post response
    mock_httpx_post.return_value.status_code = 200

    # Send a request to the scan endpoint
    response = client.post("/scan/")

    # Assert the response from the FastAPI route
    assert response.status_code == 200


def test_scan_qr_no_code(mock_httpx_post):
    # Simulate a case where no QR code is detected within the time limit
    with patch("app.scanner.QRScanner.scan") as mock_scan:
        mock_scan.return_value = None  # Simulate no QR code found

        # Call the scan endpoint
        response = client.post("/scan/")

        # Assert the response indicates no QR code found
        assert response.status_code == 200
        assert response.json() == {"message": "There was no QR code detected"}


def test_scan_qr_http_error(mock_httpx_post):
    # Simulate an HTTP error response when sending data
    mock_httpx_post.return_value.status_code = 400  # Bad Request

    # Simulate that the scan detects a QR code
    with patch("app.services.scanner.QRScanner.scan") as mock_scan:
        mock_scan.return_value = "test_qr_code_data"

        response = client.post("/scan/")

        # Assert that the FastAPI route raises an HTTPException
        assert response.status_code == 400
        assert response.json()["detail"] == "Failed to send data"


def test_scan_qr_general_exception(mock_httpx_post):
    # Simulate a general exception occurring during the HTTP request
    mock_httpx_post.side_effect = Exception("General Error")

    # Simulate that the scan detects a QR code
    with patch("app.services.scanner.QRScanner.scan") as mock_scan:
        mock_scan.return_value = "test_qr_code_data"

        response = client.post("/scan/")

        # Assert that the FastAPI route raises an HTTPException
        assert response.status_code == 500
        assert response.json()["detail"] == "General Error"
