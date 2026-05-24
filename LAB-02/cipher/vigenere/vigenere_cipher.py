class VigenereCipher:
    def __init__(self):
        pass
    def vigenere_encrypt(self, plain_text, key):
       encrypted_text = ""
       key_index = 0
       for char in plain_text:
           if char.isalpha():
                shift = ord(key[key_index % len(key)].lower()) - ord('a')
                encrypted_char = chr((ord(char.lower()) - ord('a') + shift) % 26 + ord('a'))
                if char.isupper():
                     encrypted_char = encrypted_char.upper()
                encrypted_text += encrypted_char
                key_index += 1
       return encrypted_text
    def vigenere_decrypt(self, encrypted_text, key):
        decrypted_text = ""
        key_index = 0
        for char in encrypted_text:
            if char.isalpha():
                shift = ord(key[key_index % len(key)].lower()) - ord('a')
                decrypted_char = chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
                if char.isupper():
                    decrypted_char = decrypted_char.upper()
                decrypted_text += decrypted_char
                key_index += 1
        return decrypted_text