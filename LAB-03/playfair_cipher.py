import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.playfair import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.btnEncrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btnDecrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/encrypt"
        key_val = self.ui.txtKey.toPlainText().strip()
        plain_text = self.ui.txtPlainText.toPlainText()

        if not key_val:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Vui lòng nhập Key cho Playfair!")
            return
            
        # RÀNG BUỘC: Key của Playfair phải là chữ cái Alphabet (Tạo ma trận từ khóa chữ)
        if not key_val.isalpha():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Key của Playfair chỉ được chứa các chữ cái Alphabet (A-Z, a-z)! Không chứa số.")
            return

        payload = {
            "plain_text": plain_text,
            "key": key_val
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txtCipherText.setText(data["encrypted_message"])
                QMessageBox.information(self, "Thành Công", "Playfair Encrypted Successfully")
            else:
                QMessageBox.critical(self, "Lỗi Hệ Thống", "Error while calling API Backend")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/playfair/decrypt"
        key_val = self.ui.txtKey.toPlainText().strip()
        cipher_text = self.ui.txtCipherText.toPlainText()

        if not key_val:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Vui lòng nhập Key cho Playfair!")
            return
            
        # RÀNG BUỘC: Key của Playfair phải là chữ cái Alphabet
        if not key_val.isalpha():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Key của Playfair chỉ được chứa các chữ cái Alphabet (A-Z, a-z)! Không chứa số.")
            return

        payload = {
            "cipher_text": cipher_text,
            "key": key_val
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txtPlainText.setText(data["decrypted_message"])
                QMessageBox.information(self, "Thành Công", "Playfair Decrypted Successfully")
            else:
                QMessageBox.critical(self, "Lỗi Hệ Thống", "Error while calling API Backend")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())