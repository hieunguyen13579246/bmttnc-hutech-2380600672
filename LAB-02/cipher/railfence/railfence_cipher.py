class RailFenceCipher:
    def __init__(self):
        pass

    def rail_fence_encrypt(self, plain_text, num_rails):
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
                rail_index += direction  # Đã sửa: viết đúng tên biến và đưa ra ngoài if-elif

        # Đã sửa: Đưa đoạn gom chuỗi và return ra ngoài hẳn vòng lặp for
        cipher_text = ''.join([''.join(rail) for rail in rails])
        return cipher_text

    def rail_fence_decrypt(self, cipher_text, num_rails):
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

        # Đã sửa: Đưa toàn bộ đoạn code giải mã dưới đây ra ngoài vòng lặp dựng rails
        plain_text = ""
        rail_index = 0
        direction = 1  # Đã sửa: gán giá trị rõ ràng cho biến direction
        for _ in range(len(cipher_text)):
            plain_text += rails[rail_index].pop(0)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        return plain_text