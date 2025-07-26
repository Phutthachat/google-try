from PIL import Image
import qrcode

url = "https://account-googie.onrender.com"
img = qrcode.make(url)
img.save("qr_login_page.png")

secret_msg = "In linguistics and grammar, a sentence is a linguistic expression, such as the English example The quick brown fox jumps over the lazy dog." 
binary_msg = ''.join(format(ord(c), '08b') for c in secret_msg) + '1111111111111110'  # 16-bit stopper

img = Image.open("qr_login_page.png").convert("RGB")
pixels = img.load()
width, height = img.size

# LSB
data_index = 0
for y in range(height):
    for x in range(width):
        if data_index < len(binary_msg):
            r, g, b = pixels[x, y]
            # Change Red channel
            r = (r & ~1) | int(binary_msg[data_index])
            pixels[x, y] = (r, g, b)
            data_index += 1

img.save("qr_with_secret.png")
print("QR code with secret saved as qr_with_secret.png")
