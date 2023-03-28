# -*- coding: utf-8 -*-
from PyQt4.QtCore import QDate
from PyQt4.QtGui import QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QDateEdit, QMessageBox
from database import PhonebookDatabase


class EditContactDialog(QDialog):
    def __init__(self, contact_id, parent=None):
        super(EditContactDialog, self).__init__(parent)

        self.contact_id = contact_id
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
        self.save_button = QPushButton(u'Сохранить')
        self.save_button.clicked.connect(self.save_contact)
        self.cancel_button = QPushButton(u'Отмена')
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

        self.load_contact()

    def load_contact(self):
        db = PhonebookDatabase()
        contact_id_str = str(self.contact_id)
        contact = db.get_contact(contact_id_str)[0]
    
        self.last_name_edit.setText(contact[1])
        self.first_name_edit.setText(contact[2])
        self.phone_number_edit.setText(contact[3])
        self.birth_date_edit.setDate(QDate.fromString(contact[4], 'yyyy-MM-dd'))

    def save_contact(self):
        first_name = self.first_name_edit.text().toUtf8().data()
        last_name = self.last_name_edit.text().toUtf8().data()
        phone_number = self.phone_number_edit.text().toUtf8().data()
        birth_date = self.birth_date_edit.date().toString("yyyy-MM-dd").toUtf8().data()
    
        if not first_name or not last_name or not phone_number:
            QMessageBox.warning(self, u'Ошибка', u'Заполните все обязательные поля!')
            return
    
        db = PhonebookDatabase()
        db.update_contact(self.contact_id, first_name, last_name, phone_number, birth_date)
    
        QMessageBox.information(self, u'Успешно', u'Контакт обновлен!')
        self.accept()

