from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayfairCipher

app = Flask(__name__)

# =========================================================================================
# CAESAR CIPHER ALGORITHM
# =========================================================================================
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})


# =========================================================================================
# VIGENERE CIPHER ALGORITHM
# =========================================================================================
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    
    # TỰ ĐỘNG DÒ TÊN HÀM MÃ HÓA TRONG FILE CIPHER/VIGENERE.PY
    if hasattr(vigenere_cipher, 'vigenere_encrypt'):
        encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    elif hasattr(vigenere_cipher, 'encrypt_text'):
        encrypted_text = vigenere_cipher.encrypt_text(plain_text, key)
    elif hasattr(vigenere_cipher, 'encrypt'):
        encrypted_text = vigenere_cipher.encrypt(plain_text, key)
    else:
        return jsonify({'error': 'Không tìm thấy hàm mã hóa trong class VigenereCipher'}), 500
        
    return jsonify({'encrypted_message': encrypted_text})


@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    
    # TỰ ĐỘNG DÒ TÊN HÀM GIẢI MÃ TRONG FILE CIPHER/VIGENERE.PY
    if hasattr(vigenere_cipher, 'vigenere_decrypt'):
        decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
    elif hasattr(vigenere_cipher, 'decrypt_text'):
        decrypted_text = vigenere_cipher.decrypt_text(cipher_text, key)
    elif hasattr(vigenere_cipher, 'decrypt'):
        decrypted_text = vigenere_cipher.decrypt(cipher_text, key)
    else:
        return jsonify({'error': 'Không tìm thấy hàm giải mã trong class VigenereCipher'}), 500
        
    return jsonify({'decrypted_message': decrypted_text})


# =========================================================================================
# RAILFENCE CIPHER ALGORITHM
# =========================================================================================
railfence_cipher = RailFenceCipher()

@app.route('/api/railfence/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = int(data['key'])
    
    # TỰ ĐỘNG DÒ TÊN HÀM TRONG THƯ VIỆN GỐC CỦA BẠN
    if hasattr(railfence_cipher, 'rail_fence_encrypt'):
        encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
    elif hasattr(railfence_cipher, 'encrypt_text'):
        encrypted_text = railfence_cipher.encrypt_text(plain_text, key)
    elif hasattr(railfence_cipher, 'encrypt'):
        encrypted_text = railfence_cipher.encrypt(plain_text, key)
    else:
        return jsonify({'error': 'Không tìm thấy hàm mã hóa RailFence'}), 500
        
    return jsonify({'encrypted_message': encrypted_text})

@app.route('/api/railfence/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = int(data['key'])
    
    # TỰ ĐỘNG DÒ TÊN HÀM TRONG THƯ VIỆN GỐC CỦA BẠN
    if hasattr(railfence_cipher, 'rail_fence_decrypt'):
        decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
    elif hasattr(railfence_cipher, 'decrypt_text'):
        decrypted_text = railfence_cipher.decrypt_text(cipher_text, key)
    elif hasattr(railfence_cipher, 'decrypt'):
        decrypted_text = railfence_cipher.decrypt(cipher_text, key)
    else:
        return jsonify({'error': 'Không tìm thấy hàm giải mã RailFence'}), 500
        
    return jsonify({'decrypted_message': decrypted_text})


# =========================================================================================
# PLAYFAIR CIPHER ALGORITHM
# =========================================================================================
playfair_cipher = PlayfairCipher() 

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    data = request.json
    key = data['key']
    # Nếu file gốc đặt tên là create_matrix thì đổi tên hàm lại cho đúng nhé
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({"playfair_matrix": playfair_matrix})


@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.json
    plain_text = data['plain_text']
    key = data['key']
    
    # THỬ NGHIỆM: Truyền thẳng plain_text và chuỗi key ban đầu vào hàm
    try:
        encrypted_text = playfair_cipher.encrypt_text(plain_text, key)
    except AttributeError:
        encrypted_text = playfair_cipher.playfair_encrypt(plain_text, key)
        
    return jsonify({'encrypted_message': encrypted_text})


@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    key = data['key']
    
    # THỬ NGHIỆM: Truyền thẳng cipher_text và chuỗi key ban đầu vào hàm
    try:
        decrypted_text = playfair_cipher.decrypt_text(cipher_text, key)
    except AttributeError:
        decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, key)
        
    return jsonify({'decrypted_message': decrypted_text})
# =========================================================================================
# MAIN FUNCTION
# =========================================================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)