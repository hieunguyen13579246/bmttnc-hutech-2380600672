class RailFenceCipher:
    def __init__(self):
        pass

    # ĐỔI TÊN HÀM: Thành encrypt_text và đổi num_rails thành key để khớp với app.py
    def encrypt_text(self, plain_text, key):
        num_rails = key # Gán key vào num_rails để giữ nguyên logic bên dưới của bạn
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1
        for char in plain_text:
            if char.isalpha():
                rails[rail_index].append(char)
                if rail_index == 0:
                    direction = 1
                elif rail_index == num_rails - 1:
                    direction = -1
                rail_index += direction  

        cipher_text = ''.join([''.join(rail) for rail in rails])
        return cipher_text

    # ĐỔI TÊN HÀM: Thành decrypt_text và đổi num_rails thành key để khớp với app.py
    def decrypt_text(self, cipher_text, key):
        num_rails = key # Gán key vào num_rails để giữ nguyên logic bên dưới của bạn
        rails_lengths = [0] * num_rails
        rail_index = 0
        direction = 1
        for _ in range(len(cipher_text)):
            rails_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        rails = []
        start = 0
        for length in rails_lengths:
            rails.append(list(cipher_text[start:start + length]))
            start += length

        plain_text = ""
        rail_index = 0
        direction = 1  
        for _ in range(len(cipher_text)):
            plain_text += rails[rail_index].pop(0)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        return plain_text