from PIL import Image

# --- STEP 1: โหลดรูป QR ที่ฝังข้อความไว้ ---
img = Image.open("qr_with_secret.png")
pixels = img.load()
width, height = img.size

# --- STEP 2: ดึง LSB จาก Red channel ---
binary_data = ""
for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]
        binary_data += str(r & 1)

# --- STEP 3: ตัดตอนที่เจอ stopper (16 บิตสุดท้ายคือ 1111111111111110) ---
end_marker = "1111111111111110"
end_index = binary_data.find(end_marker)
if end_index != -1:
    binary_data = binary_data[:end_index]

# --- STEP 4: แปลงกลับเป็นข้อความ ---
secret = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
print("🔍 Secret message:", secret)
