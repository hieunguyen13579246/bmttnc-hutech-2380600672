import base64
import re
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# ==================== LOGIC 4 THUẬT TOÁN MÃ HÓA ====================

def caesar_cipher(text, key, mode):
    result = ""
    key = key % 26
    if mode == "decrypt": key = 26 - key
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + key) % 26 + start)
        else: result += char
    return result

def vigenere_cipher(text, key, mode):
    result = ""
    key = re.sub(r'[^A-Z]', '', key.upper())
    if not key: return text
    key_index = 0
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            if mode == "decrypt": shift = 26 - shift
            result += chr((ord(char) - start + shift) % 26 + start)
            key_index += 1
        else: result += char
    return result

def rail_fence_encrypt(text, key):
    if key <= 1 or key >= len(text): return text
    rail = [['\n' for _ in range(len(text))] for _ in range(key)]
    dir_down = False
    row, col = 0, 0
    for char in text:
        if (row == 0) or (row == key - 1): dir_down = not dir_down
        rail[row][col] = char
        col += 1
        row += 1 if dir_down else -1
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n': result.append(rail[i][j])
    return "".join(result)

def rail_fence_decrypt(cipher, key):
    if key <= 1 or key >= len(cipher): return cipher
    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]
    dir_down = None
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0: dir_down = True
        if row == key - 1: dir_down = False
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if (rail[i][j] == '*') and (index < len(cipher)):
                rail[i][j] = cipher[index]; index += 1
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0: dir_down = True
        if row == key - 1: dir_down = False
        if rail[row][col] != '\n': result.append(rail[row][col]); col += 1
        row += 1 if dir_down else -1
    return "".join(result)

def prepare_playfair_key(key):
    key = key.upper().replace('J', 'I')
    clean_key = "".join([c for c in key if c.isalpha()])
    unique_key = ""
    for char in clean_key:
        if char not in unique_key: unique_key += char
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in unique_key: unique_key += char
    return [list(unique_key[i:i+5]) for i in range(0, 25, 5)]

def find_playfair_position(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char: return r, c
    return 0, 0

def playfair_cipher(text, key, mode):
    matrix = prepare_playfair_key(key)
    text = text.upper().replace('J', 'I')
    clean_text = "".join([c for c in text if c.isalpha()])
    if not clean_text: return ""
    if mode == "encrypt":
        prepared_text = ""
        i = 0
        while i < len(clean_text):
            prepared_text += clean_text[i]
            if i + 1 < len(clean_text):
                if clean_text[i] == clean_text[i+1]: prepared_text += "X"; i += 1
                else: prepared_text += clean_text[i+1]; i += 2
            else: prepared_text += "X"; i += 1
        clean_text = prepared_text
    result = ""
    step = 1 if mode == "encrypt" else -1
    for i in range(0, len(clean_text), 2):
        if i + 1 >= len(clean_text): break
        r1, c1 = find_playfair_position(matrix, clean_text[i])
        r2, c2 = find_playfair_position(matrix, clean_text[i+1])
        if r1 == r2:  
            result += matrix[r1][(c1 + step) % 5]
            result += matrix[r2][(c2 + step) % 5]
        elif c1 == c2:  
            result += matrix[(r1 + step) % 5][c1]
            result += matrix[(r2 + step) % 5][c2]
        else:  
            result += matrix[r1][c2]; result += matrix[r2][c1]
    return result

# ==================== ĐỊNH TUYẾN API CHÍNH ====================

@app.route('/api/cipher', methods=['POST'])
def handle_cipher():
    data = request.json
    cipher_type = data.get('type')  
    mode = data.get('mode')         
    key = data.get('key', '').strip()
    text = data.get('text', '')

    if not key or not text:
        return jsonify({'error': 'Vui lòng nhập đầy đủ cả Key và Nội dung dữ liệu!'}), 400

    try:
        if cipher_type == 'caesar': result = caesar_cipher(text, int(key), mode)
        elif cipher_type == 'vigenere': result = vigenere_cipher(text, key, mode)
        elif cipher_type == 'railfence':
            if int(key) <= 0: return jsonify({'error': 'Số hàng rào bắt buộc phải lớn hơn 0!'}), 400
            result = rail_fence_encrypt(text, int(key)) if mode == 'encrypt' else rail_fence_decrypt(text, int(key))
        elif cipher_type == 'playfair': result = playfair_cipher(text, key, mode)
        else: return jsonify({'error': 'Thuật toán không hợp lệ!'}), 400
        return jsonify({'result': result})
    except ValueError:
        return jsonify({'error': 'Lỗi định dạng cấu trúc Khóa (Key)! Hãy kiểm tra lại.'}), 400

# ==================== API GIẤU TIN XUẤT ẢNH CHO PHÉP DOWNLOAD ====================

@app.route('/api/stego/hide', methods=['POST'])
def stego_hide():
    data = request.json
    image_base64 = data.get('image')
    text_to_hide = data.get('text', '').strip()

    if not image_base64 or not text_to_hide:
        return jsonify({'error': 'Ràng buộc: Thiếu file hình ảnh hoặc nội dung cần giấu!'}), 400

    try:
        header, encoded = image_base64.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        pixels = img.load()
        width, height = img.size
        
        full_text = text_to_hide + "\0"
        binary_text = "".join([format(ord(c), '08b') for c in full_text])
        
        max_capacity = width * height * 3
        if len(binary_text) > max_capacity:
            return jsonify({'error': f'Lỗi dung lượng: Ảnh chỉ chứa được {max_capacity} bits, chữ của em chiếm {len(binary_text)} bits!'}), 400
        
        bit_idx = 0
        text_len = len(binary_text)
        for y in range(height):
            for x in range(width):
                if bit_idx >= text_len: break
                r, g, b = pixels[x, y]
                if bit_idx < text_len: r = (r & ~1) | int(binary_text[bit_idx]); bit_idx += 1
                if bit_idx < text_len: g = (g & ~1) | int(binary_text[bit_idx]); bit_idx += 1
                if bit_idx < text_len: b = (b & ~1) | int(binary_text[bit_idx]); bit_idx += 1
                pixels[x, y] = (r, g, b)
                
        buffered = BytesIO()
        img.save(buffered, format="PNG") # Lưu dạng định dạng PNG để không bị mất mát bit màu
        saved_base64 = header + "," + base64.b64encode(buffered.getvalue()).decode()
        
        # Trả ngược chuỗi ảnh đã giấu tin mật về cho Client tải xuống
        return jsonify({
            'message': 'Đã xử lý giấu tin nhắn vào dữ liệu ảnh thành công!',
            'stego_image': saved_base64
        })
    except Exception as e:
        return jsonify({'error': f'Lỗi hệ thống: {str(e)}'}), 500

@app.route('/api/stego/extract', methods=['POST'])
def stego_extract():
    data = request.json
    image_base64 = data.get('image')

    if not image_base64:
        return jsonify({'error': 'Không tìm thấy hình ảnh hợp lệ để bóc tách!'}), 400

    try:
        _, encoded = image_base64.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        pixels = img.load()
        width, height = img.size
        
        extracted_bits = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                extracted_bits.append(str(r & 1))
                extracted_bits.append(str(g & 1))
                extracted_bits.append(str(b & 1))
                
        all_bits = "".join(extracted_bits)
        extracted_text = ""
        for i in range(0, len(all_bits), 8):
            byte = all_bits[i:i+8]
            if len(byte) < 8: break
            char_code = int(byte, 2)
            if char_code == 0: break
            extracted_text += chr(char_code)
            
        return jsonify({'extracted_text': extracted_text if extracted_text else "Không tìm thấy dữ liệu tin ẩn."})
    except Exception as e:
        return jsonify({'error': f'Lỗi bóc tách LSB: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)