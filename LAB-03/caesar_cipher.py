import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối sự kiện nút bấm
        self.ui.btnEncrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btnDecrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        key_raw = self.ui.txtKey.toPlainText().strip()
        plain_text = self.ui.txtPlainText.toPlainText()

        # RÀNG BUỘC: Kiểm tra số nguyên
        if not key_raw.isdigit():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Key của Caesar bắt buộc phải là một số nguyên!")
            return
            
        key_val = int(key_raw)
        # RÀNG BUỘC: Khoảng giá trị từ 0 đến 26
        if key_val < 0 or key_val > 26:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Key của Caesar phải nằm trong khoảng từ 0 đến 26!")
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
                QMessageBox.information(self, "Thành Công", "Caesar Encrypted Successfully")
            else:
                QMessageBox.critical(self, "Lỗi Hệ Thống", "Error while calling API Backend")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        key_raw = self.ui.txtKey.toPlainText().strip()
        cipher_text = self.ui.txtCipherText.toPlainText()

        # RÀNG BUỘC: Kiểm tra số nguyên
        if not key_raw.isdigit():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Key của Caesar bắt buộc phải là một số nguyên!")
            return
            
        key_val = int(key_raw)
        # RÀNG BUỘC: Khoảng giá trị từ 0 đến 26
        if key_val < 0 or key_val > 26:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Key của Caesar phải nằm trong khoảng từ 0 đến 26!")
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
                QMessageBox.information(self, "Thành Công", "Caesar Decrypted Successfully")
            else:
                QMessageBox.critical(self, "Lỗi Hệ Thống", "Error while calling API Backend")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())