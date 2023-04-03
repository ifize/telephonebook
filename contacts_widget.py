# -*- coding: utf-8 -*-
from datetime import datetime

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
                         QScrollArea, QHeaderView, QPushButton, QDialog, QMessageBox, QHBoxLayout)

from database import PhonebookDatabase
from add_contact_widget import AddContactWidget
from edit_contact_widget import EditContactDialog


class ContactsWidget(QWidget):
    def __init__(self, parent=None):
        super(ContactsWidget, self).__init__(parent)
        self.current_filter = None
        print("Creating ContactsWidget")
        self.initUI()

    def initUI(self):
        # создаем таблицу с заголовками столбцов
        self.contacts_table = QTableWidget(self)
        self.contacts_table.setColumnCount(4)
        self.contacts_table.setHorizontalHeaderLabels([u'Фамилия', u'Имя', u'Телефон', u'Дата рождения'])

        # добавляем строки в таблицу
        db = PhonebookDatabase()
        contacts = db.get_contacts()
        self.contacts_table.setRowCount(len(contacts))  # и здесь
        for i, contact in enumerate(contacts):
            self.contacts_table.setItem(i, 0, QTableWidgetItem(contact['last_name']))
            self.contacts_table.item(i, 0).setData(Qt.UserRole, contact['id'])
            self.contacts_table.setItem(i, 1, QTableWidgetItem(contact['first_name']))  # и здесь
            self.contacts_table.setItem(i, 2, QTableWidgetItem(contact['phone_number']))  # и здесь
            self.contacts_table.setItem(i, 3, QTableWidgetItem(contact['birth_date']))  # и здесь

        # делаем растягивание таблицы на всю доступную область
        self.contacts_table.horizontalHeader().setStretchLastSection(True)
        self.contacts_table.verticalHeader().setVisible(False)
        self.contacts_table.resizeColumnsToContents()
        self.contacts_table.resizeRowsToContents()
        self.contacts_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.contacts_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.contacts_table.setSelectionMode(QTableWidget.SingleSelection)

        # создаем QScrollArea
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.contacts_table)  # и здесь

        # добавляем QScrollArea в главный QVBoxLayout
        layout = QVBoxLayout(self)
        layout.addWidget(scroll)
        buttons_layout = QHBoxLayout()

        add_button = QPushButton(u"Добавить", self)
        add_button.clicked.connect(self.add_contact)
        buttons_layout.addWidget(add_button)

        edit_button = QPushButton(u"Редактировать", self)
        edit_button.clicked.connect(self.edit_contact)
        buttons_layout.addWidget(edit_button)

        delete_button = QPushButton(u"Удалить", self)
        delete_button.clicked.connect(self.delete_contact)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)

        # подстраиваем таблицу под размеры виджета при изменении размера
        self.contacts_table.horizontalHeader().setResizeMode(QHeaderView.Stretch)  # и здесь
        self.contacts_table.verticalHeader().setResizeMode(QHeaderView.Stretch)  # и здесь
        self.contacts_table.resizeColumnsToContents()  # и здесь
        self.contacts_table.resizeRowsToContents()  # и здесь

    def filter_contacts_by_alphabet(self, letter):
        self.current_filter = letter
        self.update_contact()

    def delete_contact(self):
        selected_rows = self.contacts_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, u"Удаление контакта", u"Пожалуйста, выберите контакт для удаления.")
            return
    
        selected_row = selected_rows[0].row()
        contact_id = self.contacts_table.item(selected_row, 0).data(Qt.UserRole).toString()
    
        reply = QMessageBox.question(self, u"Удаление контакта",
                                     u"Вы уверены, что хотите удалить выбранный контакт?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
        if reply == QMessageBox.Yes:
            db = PhonebookDatabase()
            db.delete_contact(str(contact_id))
            self.update_contact()

    def update_contact(self):
        db = PhonebookDatabase()
    
        if self.current_filter:
            first_letter, last_letter = self.current_filter.split('-')
            contacts = db.get_contacts_by_alphabet(first_letter, last_letter)
        else:
            contacts = db.get_contacts()
    
        # Очистить таблицу
        self.contacts_table.setRowCount(0)
    
        # Заполнить таблицу обновленными контактами
        self.contacts_table.setRowCount(len(contacts))
        for i, contact in enumerate(contacts):
            self.contacts_table.setItem(i, 0, QTableWidgetItem(contact['last_name']))
            self.contacts_table.setItem(i, 1, QTableWidgetItem(contact['first_name']))
            self.contacts_table.setItem(i, 2, QTableWidgetItem(contact['phone_number']))
            birth_date = datetime.strptime(contact['birth_date'], '%Y-%m-%d')
            self.contacts_table.setItem(i, 3, QTableWidgetItem(birth_date.strftime('%Y-%m-%d')))

    def add_contact(self):
        add_contact_widget = AddContactWidget(self)
        result = add_contact_widget.exec_()
    
        if result == QDialog.Accepted:
            self.update_contact()

    def edit_contact(self):
        selected_items = self.contacts_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, u'Ошибка', u'Выберите контакт для редактирования!')
            return
    
        contact_id = selected_items[0].data(Qt.UserRole)
        if not contact_id.isValid():
            QMessageBox.warning(self, u'Ошибка', u'Не удалось получить идентификатор контакта!')
            return
    
        contact_id = int(contact_id.toPyObject())
        edit_contact_dialog = EditContactDialog(contact_id, self)
        result = edit_contact_dialog.exec_()
        if result == QDialog.Accepted:
            self.update_contact()


