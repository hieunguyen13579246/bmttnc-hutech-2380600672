import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.btnEncrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btnDecrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        key_raw = self.ui.txtKey.toPlainText().strip()
        plain_text = self.ui.txtPlainText.toPlainText()

        # RÀNG BUỘC: Kiểm tra số nguyên dương (Vì Rail Fence cần số hàng/tầng để xếpzigzag)
        if not key_raw.isdigit():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Key (Số tầng) của Rail Fence bắt buộc phải là một số nguyên dương!")
            return
            
        key_val = int(key_raw)
        if key_val < 2:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Số tầng (Key) của Rail Fence phải lớn hơn hoặc bằng 2!")
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
                QMessageBox.information(self, "Thành Công", "Rail Fence Encrypted Successfully")
            else:
                QMessageBox.critical(self, "Lỗi Hệ Thống", "Error while calling API Backend")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        key_raw = self.ui.txtKey.toPlainText().strip()
        cipher_text = self.ui.txtCipherText.toPlainText()

        # RÀNG BUỘC: Kiểm tra số nguyên dương
        if not key_raw.isdigit():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Key (Số tầng) của Rail Fence bắt buộc phải là một số nguyên dương!")
            return
            
        key_val = int(key_raw)
        if key_val < 2:
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Số tầng (Key) của Rail Fence phải lớn hơn hoặc bằng 2!")
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
                QMessageBox.information(self, "Thành Công", "Rail Fence Decrypted Successfully")
            else:
                QMessageBox.critical(self, "Lỗi Hệ Thống", "Error while calling API Backend")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())