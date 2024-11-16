from datetime import datetime, timedelta

import qrcode
from qrcode.main import QRCode


def generate_qr_code(data, filename) -> None:
    qr = QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)


# Get today's and yesterday's dates in a simple format
today_date = datetime.now().strftime("%Y-%m-%d")
yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# Generate QR codes with the dates as data
generate_qr_code(today_date, "../qr_codes/qr_today.png")
generate_qr_code(yesterday_date, "../qr_codes/qr_yesterday.png")
