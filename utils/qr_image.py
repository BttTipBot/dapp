
import qrcode
import io

# Create a QR code
def qrcode_create(address):
    print("qrcode_create: address:", address)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(address)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)  # Reset the stream position to the start

    return buf