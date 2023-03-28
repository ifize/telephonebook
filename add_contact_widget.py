# -*- coding: utf-8 -*-
from PyQt4.QtGui import QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QDateEdit, QMessageBox
from database import PhonebookDatabase


class AddContactWidget(QDialog):
    def __init__(self, parent=None):
        super(AddContactWidget, self).__init__(parent)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.first_name_label = QLabel(u'Имя')
        self.first_name_edit = QLineEdit()
        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_edit)

        self.last_name_label = QLabel(u'Фамилия')
        self.last_name_edit = QLineEdit()
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_edit)

        self.phone_number_label = QLabel(u'Телефон')
        self.phone_number_edit = QLineEdit()
        layout.addWidget(self.phone_number_label)
        layout.addWidget(self.phone_number_edit)

        self.birth_date_label = QLabel(u'Дата рождения')
        self.birth_date_edit = QDateEdit()
        layout.addWidget(self.birth_date_label)
        layout.addWidget(self.birth_date_edit)

        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton(u'Добавить')
        self.add_button.clicked.connect(self.add_contact)
        self.cancel_button = QPushButton(u'Отмена')
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def add_contact(self):
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()
        phone_number = self.phone_number_edit.text()
        birth_date = self.birth_date_edit.date().toString('yyyy-MM-dd')

        if not first_name or not last_name or not phone_number:
            QMessageBox.warning(self, u'Ошибка', u'Заполните все обязательные поля!')
            return

        db = PhonebookDatabase()
        success = db.add_contact(first_name, last_name, phone_number, birth_date)

        if success:
            QMessageBox.information(self, u'Успешно', u'Контакт добавлен!')
            self.accept()
        else:
            QMessageBox.warning(self, u'Ошибка', u'Не удалось добавить контакт!')
