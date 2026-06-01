import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # SỬA TẠI ĐÂY: Kiểm tra xem giao diện đang dùng biến nào để tự động kết nối, tránh lỗi tuyệt đối
        if hasattr(self.ui, 'btnEncrypt'):
            self.ui.btnEncrypt.clicked.connect(self.call_api_encrypt)
            self.ui.btnDecrypt.clicked.connect(self.call_api_decrypt)
        elif hasattr(self.ui, 'btn_encrypt'):
            self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
            self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        else:
            print("CẢNH BÁO: Không tìm thấy nút bấm Encrypt/Decrypt nào trên giao diện ui!")

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        payload = {
            "plain_text": self.ui.txtPlainText.toPlainText(),  # Đã sửa
           "key": self.ui.txtKey.toPlainText()                   # Đã sửa
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txtCipherText.setText(data["encrypted_message"])  # Đã sửa

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        payload = {
            "cipher_text": self.ui.txtCipherText.toPlainText(),  # Đã sửa
            "key": self.ui.txtKey.toPlainText()                       # Đã sửa
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txtPlainText.setText(data["decrypted_message"])  # Đã sửa

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print("Error: %s" % e.message)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())