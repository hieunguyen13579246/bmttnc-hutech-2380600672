class PlayfairCipher:
    def __init__(self): 
        pass

    def create_playfair_matrix(self, key):
        # Đã sửa: Viết đúng chính tả tên hàm thành create_playfair_matrix
        key = key.upper().replace("J", "I")
        
        # Lọc lấy các ký tự duy nhất trong key theo đúng thứ tự xuất hiện
        matrix = []
        for letter in key:
            if letter.isalpha() and letter not in matrix:
                matrix.append(letter)
                
        # Điền nốt các ký tự còn thiếu trong Alphabet vào ma trận
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for letter in alphabet:
            if letter not in matrix:
                matrix.append(letter)
                
        playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        return None

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = plain_text.upper().replace("J", "I")
        # Loại bỏ khoảng trắng nếu có để tránh lỗi tìm tọa độ
        plain_text = "".join([c for c in plain_text if c.isalpha()])
        
        # Xử lý chèn X nếu có 2 ký tự trùng nhau đứng cạnh nhau hoặc chuỗi lẻ
        prepared_text = ""
        i = 0
        while i < len(plain_text):
            prepared_text += plain_text[i]
            if i + 1 < len(plain_text):
                if plain_text[i] == plain_text[i+1]:
                    prepared_text += "X"
                    i += 1
                else:
                    prepared_text += plain_text[i+1]
                    i += 2
            else:
                prepared_text += "X"
                i += 1

        encrypted_text = ""
        for i in range(0, len(prepared_text), 2):
            pair = prepared_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5]
                encrypted_text += matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1]
                encrypted_text += matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2]
                encrypted_text += matrix[row2][col1]
                
        return encrypted_text  # Đã sửa: Đưa lệnh return ra ngoài hẳn vòng lặp for

    def playfair_decrypt(self, encrypted_text, matrix):
        cipher_text = encrypted_text.upper()
        decrypted_text = ""
        
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]
                
        return decrypted_text  # Trả về chuỗi giải mã đầy đủ chuẩn xác