import sys
from pocket_advisor_gui import PocketAdvisorGUI
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
pa = PocketAdvisorGUI()
pa.show()
sys.exit(app.exec_())
