# -*- coding: utf-8 -*-
from PyQt4.QtGui import QWidget, QVBoxLayout, QPushButton

class AlphabetWidget(QWidget):
    def __init__(self, parent=None):
        super(AlphabetWidget, self).__init__(parent)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        alphabet = [u'А-В', u'Г-Ж', u'З-К', u'Л-М', u'Н-О', u'П-Р', u'С-Т', u'У-Ф', u'Х-Ц', u'Ч-Ш', u'Щ-Э', u'Ю-Я']

        for letter in alphabet:
            button = QPushButton(letter, self)
            button.clicked.connect(lambda state, l=letter: self.on_alphabet_button_click(l))
            layout.addWidget(button)

    def on_alphabet_button_click(self, letter):
        self.parent().parent().filter_contacts_by_alphabet(letter)
