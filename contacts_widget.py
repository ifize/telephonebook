# -*- coding: utf-8 -*-

from PyQt4.QtGui import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QScrollArea, QHeaderView

from database import PhonebookDatabase


class ContactsWidget(QWidget):
    def __init__(self, parent=None):
        super(ContactsWidget, self).__init__(parent)
        print("Creating ContactsWidget")
        self.initUI()

    def initUI(self):
        # создаем таблицу с заголовками столбцов
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([u'Фамилия', u'Имя', u'Телефон', u'Дата рождения'])

        # добавляем строки в таблицу
        db = PhonebookDatabase()
        contacts = db.get_contacts()
        self.table.setRowCount(len(contacts))
        for i, contact in enumerate(contacts):
            self.table.setItem(i, 0, QTableWidgetItem(contact['last_name']))
            self.table.setItem(i, 1, QTableWidgetItem(contact['first_name']))
            self.table.setItem(i, 2, QTableWidgetItem(contact['phone_number']))
            self.table.setItem(i, 3, QTableWidgetItem(contact['birth_date']))

        # делаем растягивание таблицы на всю доступную область
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        # создаем QScrollArea
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.scrollContent = QWidget(scroll)
        scroll.setWidget(self.scrollContent)

        # добавляем таблицу в виджет scrollContent
        layout = QVBoxLayout(self.scrollContent)
        layout.addWidget(self.table)

        # подстраиваем таблицу под размеры виджета при изменении размера
        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        # подстраиваем размеры таблицы под размеры scrollContent
        self.scrollContent.setMinimumSize(self.table.sizeHint())
        self.table.setMinimumSize(self.scrollContent.sizeHint())
