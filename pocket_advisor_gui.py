from PyQt5.QtWidgets import *
from chat_bot import ChatBot
from pocket_advisor import SpeechToText
from text_to_speech import TextToSpeech
import asyncio
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class PocketAdvisorGUI(QDialog):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
        QToolButton {
            width: 50;
            height: 50;
            text-align: center;
        }
        QLineEdit {
            padding: 10;
        }
        QDialog {
            background-color: rgb(51, 51, 51);
        }
        """)

        layout = QVBoxLayout()

        self.browser = QTextBrowser()
        self.browser.setStyleSheet("""
        color: white;
        font-size: 15px;
        background-color: rgb(81, 81, 81);
        
        """)
        self.browser.openExternalLinks()
        self.mic_icon = QToolButton(icon=QIcon("microphone.png"))
        self.mute_icon = QPushButton("muted.png")
        self.message_box = QLineEdit()
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.mic_icon)
        layout.addWidget(self.browser)
        layout.addLayout(self.button_layout)
        layout.addWidget(self.message_box)

        self.setLayout(layout)
        self.setWindowTitle("Pocket Advisor")
        self.resize(300, 600)
        self.move(200, 0)
        self.message_box.setFocus()

        self.first_message = True
        self.con_id = None
        self.greeting()
        # Connections
        self.message_box.returnPressed.connect(self.send_message)
        self.mic_icon.clicked.connect(self.send_voice)

    def send_message(self):
        try:
            message = self.message_box.text()
            self.browser.append("<p>You: " + message + "</p>")
            self.message_box.clear()

            self.receive_message(message)

        except Exception as e:
            print(e)

    def receive_message(self, message):
        try:
            chat_bot = ChatBot(message)
            if self.con_id is None:
                response = chat_bot.send_message(self.first_message)
            else:
                response = chat_bot.send_message(self.first_message, self.con_id)
            output = response[0]
            self.con_id = response[1]
            self.browser.append("<p>Agent: " + output + "</p>")
            self.first_message = False
            TextToSpeech(output)
        except Exception as e:
            print(e)

    def send_voice(self):
        try:
            result = SpeechToText().run()
            self.browser.append("You: " + result)
            print(result)
            self.receive_message(result)
        except Exception as e:
            print(e)

    def greeting(self):
        try:
            chat_bot = ChatBot(None)
            response = chat_bot.send_message(self.first_message)
            output = response[0]
            self.con_id = response[1]
            self.browser.append("<p>Agent: " + output+"</p>")
            self.first_message = False
            TextToSpeech(output)
        except Exception as e:
            print(e)