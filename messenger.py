import requests
from PyQt5 import QtWidgets

import messengerui


class MessengerApp(QtWidgets.QMainWindow, messengerui.Ui_Messenger):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.sendButton.pressed.connect(self.send_message)

    def send_message(self):
        name = self.nameInput.text()
        text = self.textInput.toPlainText()
        try:
            response = requests.post(
                'http://127.0.0.1:5000/send',
                json={'text': text, 'name': name}
            )
        except:
            self.messagesBrowser.append('Сервер недоступен. Попробуйте позднее')
            self.messagesBrowser.append('')
            self.messagesBrowser.repaint()
            return

        if response.status_code == 400:
            self.messagesBrowser.append('Неправильные имя и/или пароль')
            self.messagesBrowser.append('')
            self.messagesBrowser.repaint()
            return

        self.textInput.clear()
        self.textInput.repaint()


app = QtWidgets.QApplication([])
window = MessengerApp()
window.show()
app.exec_()