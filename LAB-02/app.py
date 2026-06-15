import base64
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# ==================== LOGIC THUẬT TOÁN MÃ HÓA ====================

# 1. CAESAR CIPHER
def caesar_cipher(text, key, mode):
    result = ""
    key = key % 26
    if mode == "decrypt":
        key = 26 - key
        
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - start + key) % 26 + start)
        else:
            result += char
    return result


# 2. VIGENERE CIPHER
def vigenere_cipher(text, key, mode):
    result = ""
    key = key.upper()
    key_index = 0
    
    if not key:
        return text

    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            shift = ord(key[key_index % len(key)]) - ord('A')
            
            if mode == "decrypt":
                shift = 26 - shift
                
            result += chr((ord(char) - start + shift) % 26 + start)
            key_index += 1  
        else:
            result += char  
            
    return result


# 3. RAIL FENCE CIPHER (Mã hóa đường rào)
def rail_fence_encrypt(text, key):
    if key == 1 or key >= len(text):
        return text
        
    rail = [['\n' for _ in range(len(text))] for _ in range(key)]
    dir_down = False
    row, col = 0, 0
    
    for char in text:
        if (row == 0) or (row == key - 1):
            dir_down = not dir_down
        rail[row][col] = char
        col += 1
        row += 1 if dir_down else -1
        
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)

def rail_fence_decrypt(cipher, key):
    if key == 1 or key >= len(cipher):
        return cipher
        
    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]
    dir_down = None
    row, col = 0, 0
    
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
            
        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1
        
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if (rail[i][j] == '*') and (index < len(cipher)):
                rail[i][j] = cipher[index]
                index += 1
                
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
            
        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1
            
        row += 1 if dir_down else -1
    return "".join(result)


# 4. PLAYFAIR CIPHER
def prepare_playfair_key(key):
    key = key.upper().replace('J', 'I')
    clean_key = ""
    for char in key:
        if char.isalpha() and char not in clean_key:
            clean_key += char
            
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    for char in alphabet:
        if char not in clean_key:
            clean_key += char
            
    return [list(clean_key[i:i+5]) for i in range(0, 25, 5)]

def find_playfair_position(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return 0, 0

def playfair_cipher(text, key, mode):
    matrix = prepare_playfair_key(key)
    text = text.upper().replace('J', 'I')
    clean_text = "".join([c for c in text if c.isalpha()])
    
    if mode == "encrypt":
        prepared_text = ""
        i = 0
        while i < len(clean_text):
            prepared_text += clean_text[i]
            if i + 1 < len(clean_text):
                if clean_text[i] == clean_text[i+1]:
                    prepared_text += "X"  
                    i += 1
                else:
                    prepared_text += clean_text[i+1]
                    i += 2
            else:
                prepared_text += "X"  
                i += 1
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
            result += matrix[r1][c2]
            result += matrix[r2][c1]
            
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
        return jsonify({'error': 'Vui lòng nhập đầy đủ Key và Nội dung!'}), 400

    try:
        if cipher_type == 'caesar':
            result = caesar_cipher(text, int(key), mode)
        elif cipher_type == 'vigenere':
            result = vigenere_cipher(text, key, mode)
        elif cipher_type == 'railfence':
            if mode == 'encrypt':
                result = rail_fence_encrypt(text, int(key))
            else:
                result = rail_fence_decrypt(text, int(key))
        elif cipher_type == 'playfair':
            result = playfair_cipher(text, key, mode)
        else:
            return jsonify({'error': 'Thuật toán không hợp lệ!'}), 400
            
        return jsonify({'result': result})
        
    except ValueError:
        return jsonify({'error': 'Lỗi định dạng Key! Hãy kiểm tra lại số hàng/số dịch chuyển.'}), 400
    except Exception as e:
        return jsonify({'error': f'Có lỗi xảy ra: {str(e)}'}), 500


# ==================== API XỬ LÝ GIẤU TIN REAL LSB (ĐÃ SỬA LỖI) ====================

# Biến tạm lưu trữ ảnh base64 sau khi đã giấu tin để Client tải về giải mã
stego_image_storage = {}

@app.route('/api/stego/hide', methods=['POST'])
def stego_hide():
    data = request.json
    image_base64 = data.get('image')
    text_to_hide = data.get('text', '').strip()

    if not image_base64 or not text_to_hide:
        return jsonify({'error': 'Vui lòng chọn ảnh và nhập nội dung cần giấu!'}), 400

    try:
        # Tách header base64 và decode dữ liệu ảnh
        header, encoded = image_base64.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        
        pixels = img.load()
        width, height = img.size
        
        # Chuyển chuỗi cần giấu + ký tự kết thúc chuỗi NULL (\0) sang hệ nhị phân 8-bit
        full_text = text_to_hide + "\0"
        binary_text = "".join([format(ord(c), '08b') for c in full_text])
        
        bit_idx = 0
        text_len = len(binary_text)
        
        # Tiến hành thay đổi bit ít quan trọng nhất LSB của từng Pixel màu
        for y in range(height):
            for x in range(width):
                if bit_idx >= text_len:
                    break
                r, g, b = pixels[x, y]
                
                if bit_idx < text_len:
                    r = (r & ~1) | int(binary_text[bit_idx])
                    bit_idx += 1
                if bit_idx < text_len:
                    g = (g & ~1) | int(binary_text[bit_idx])
                    bit_idx += 1
                if bit_idx < text_len:
                    b = (b & ~1) | int(binary_text[bit_idx])
                    bit_idx += 1
                    
                pixels[x, y] = (r, g, b)
                
        # Lưu ảnh mới đã giấu tin vào bộ nhớ đệm tạm thời
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        saved_base64 = header + "," + base64.b64encode(buffered.getvalue()).decode()
        
        # Lưu trữ lại ảnh này để phiên giải mã kế tiếp đọc được tin ẩn
        stego_image_storage['current'] = saved_base64
        
        return jsonify({'message': 'Đã xử lý giấu tin nhắn vào dữ liệu ảnh thành công!'})
    except Exception as e:
        return jsonify({'error': f'Lỗi hệ thống xử lý ảnh LSB: {str(e)}'}), 500


@app.route('/api/stego/extract', methods=['POST'])
def stego_extract():
    data = request.json
    image_base64 = data.get('image')

    # Ưu tiên lấy ảnh đã được xử lý giấu tin từ bộ nhớ nếu có
    target_image = stego_image_storage.get('current', image_base64)

    if not target_image:
        return jsonify({'error': 'Không tìm thấy dữ liệu hình ảnh để giải mã!'}), 400

    try:
        _, encoded = target_image.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        
        pixels = img.load()
        width, height = img.size
        
        extracted_bits = []
        # Quét qua dữ liệu pixel để bóc tách các bit cuối cùng ra
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                extracted_bits.append(str(r & 1))
                extracted_bits.append(str(g & 1))
                extracted_bits.append(str(b & 1))
                
        all_bits = "".join(extracted_bits)
        extracted_text = ""
        
        # Gom nhóm cụm 8 bit dịch ngược lại thành ký tự ASCII ban đầu
        for i in range(0, len(all_bits), 8):
            byte = all_bits[i:i+8]
            if len(byte) < 8: 
                break
            char_code = int(byte, 2)
            if char_code == 0:  # Gặp ký tự kết thúc NULL -> Dừng bóc tách chữ
                break
            extracted_text += chr(char_code)
            
        return jsonify({'extracted_text': extracted_text})
    except Exception as e:
        return jsonify({'error': f'Lỗi hệ thống giải mã ảnh LSB: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)