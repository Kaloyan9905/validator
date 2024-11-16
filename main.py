from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.exceptions.camera_errors import GrabFrameException
from app.scanner import QRScanner
from app.utils.ticket_expiration import ticket_is_expired

app = FastAPI()

SCAN_DURATION = 10

NO_QR_CODE_FOUND = 'There was no QR code detected'


@app.get("/scan/")
async def scan_qr() -> JSONResponse:
    qr_scanner = QRScanner()

    try:
        qr_data = await qr_scanner.scan()

        if qr_data is not None:
            if ticket_is_expired(qr_data):
                return JSONResponse({'message': 'Ticket Expired'}, status_code=200)

            return JSONResponse({'message': f'Valid Ticket'}, status_code=200)

    except GrabFrameException as exception:
        return JSONResponse({'message': str(exception)}, status_code=500)

    finally:
        await qr_scanner.release()

    return JSONResponse({'message': NO_QR_CODE_FOUND}, status_code=404)
