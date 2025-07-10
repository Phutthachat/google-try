from PIL import Image
import qrcode

# --- STEP 1: สร้าง QR code ---
url = "https://account-googie.onrender.com"
img = qrcode.make(url)
img.save("qr_login_page.png")

# --- STEP 2: เตรียมข้อความลับที่จะฝัง ---
secret_msg = "hello_world this is the limitation of code"  # ข้อความที่ต้องการฝัง
binary_msg = ''.join(format(ord(c), '08b') for c in secret_msg) + '1111111111111110'  # ใช้ 16-bit stopper

# --- STEP 3: เปิด QR และแปลงเป็น RGB ---
img = Image.open("qr_login_page.png").convert("RGB")
pixels = img.load()
width, height = img.size

# --- STEP 4: ฝังข้อมูลใน LSB ---
data_index = 0
for y in range(height):
    for x in range(width):
        if data_index < len(binary_msg):
            r, g, b = pixels[x, y]
            # เปลี่ยน LSB ของ Red channel
            r = (r & ~1) | int(binary_msg[data_index])
            pixels[x, y] = (r, g, b)
            data_index += 1

img.save("qr_with_secret.png")
print("QR code with secret saved as qr_with_secret.png")
