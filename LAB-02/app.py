from flask import Flask, render_template, request, json

# KHỞI TẠO BIẾN APP DUY NHẤT Ở ĐẦU FILE (Bắt buộc)
app = Flask(__name__)

# Trang chủ hệ thống
@app.route("/")
def home():
    return render_template('index.html')

from cipher.caesar import CaesarCipher

@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain']) 
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

##################################################################################
from cipher.playfair import PlayfairCipher

@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/encrypt_playfair", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain'] 
    
    Playfair = PlayfairCipher()
    encrypted_text = Playfair.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt_playfair", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    
    Playfair = PlayfairCipher()
    decrypted_text = Playfair.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

#################################################################################
from cipher.vigenere import VigenereCipher

@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html') 

@app.route("/encrypt_vigenere", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain'] 
    
    Vigenere = VigenereCipher()
    encrypted_text = Vigenere.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt_vigenere", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    
    Vigenere = VigenereCipher()
    decrypted_text = Vigenere.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

###############################################################################
from cipher.railfence import RailFenceCipher

@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/encrypt_railfence", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain']) 
    
    RailFence = RailFenceCipher()
    encrypted_text = RailFence.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt_railfence", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    
    RailFence = RailFenceCipher()
    decrypted_text = RailFence.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)