# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox, QDialog, QDateEdit, QVBoxLayout
from PyQt4.QtCore import QDate

from contacts_widget import ContactsWidget
from database import PhonebookDatabase


class Phonebook(QMainWindow):
    def __init__(self):
        super(Phonebook, self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle(u'Phonebook')
        # создаем объект базы данных
        self.db = PhonebookDatabase()

        # добавляем элементы управления для окна авторизации
        loginLabel = QLabel(u'Логин:', self)
        loginLabel.move(50, 50)
        self.loginInput = QLineEdit(self)
        self.loginInput.move(110, 50)
        passwordLabel = QLabel(u'Пароль:', self)
        passwordLabel.move(50, 80)
        self.passwordInput = QLineEdit(self)
        self.passwordInput.move(110, 80)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.rememberCheckbox = QCheckBox(u'Запомнить меня', self)
        self.rememberCheckbox.move(110, 110)
        loginButton = QPushButton(u'Войти', self)
        loginButton.move(50, 150)
        loginButton.clicked.connect(self.login)
        registerButton = QPushButton(u'Регистрация', self)
        registerButton.move(170, 150)
        registerButton.clicked.connect(self.register)

        self.show()

    def login(self):
        # обработчик нажатия кнопки "Войти"
        login = self.loginInput.text()
        password = self.passwordInput.text()
        remember = self.rememberCheckbox.isChecked()

        # проверяем логин и пароль в базе данных
        if self.db.check_login_password(login, password):
            print("Login successful")
            main_window = MainWindow(self)
            main_window.show()
            self.main_window = main_window
            self.hide()
        else:
            # иначе выводим всплывающее окно с ошибкой
            QMessageBox.warning(self, u'Ошибка', u'Неверный логин или пароль')

    def register(self):
        # обработчик нажатия кнопки "Регистрация"
        # открываем окно регистрации
        registerWindow = RegisterWindow()
        registerWindow.exec_()


class RegisterWindow(QDialog):
    def __init__(self):
        super(RegisterWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(u'Регистрация')
        self.setGeometry(300, 300, 350, 250)

        # добавляем элементы управления для окна регистрации
        usernameLabel = QLabel(u'Имя пользователя:', self)
        usernameLabel.move(50, 20)
        self.usernameInput = QLineEdit(self)
        self.usernameInput.move(170, 20)

        passwordLabel = QLabel(u'Пароль:', self)
        passwordLabel.move(50, 50)
        self.passwordInput = QLineEdit(self)
        self.passwordInput.move(170, 50)
        self.passwordInput.setEchoMode(QLineEdit.Password)

        confirmPasswordLabel = QLabel(u'Повторите пароль:', self)
        confirmPasswordLabel.move(50, 80)
        self.confirmPasswordInput = QLineEdit(self)
        self.confirmPasswordInput.move(170, 80)
        self.confirmPasswordInput.setEchoMode(QLineEdit.Password)

        lastnameLabel = QLabel(u'Фамилия:', self)
        lastnameLabel.move(50, 110)
        self.lastnameInput = QLineEdit(self)
        self.lastnameInput.move(170, 110)

        firstnameLabel = QLabel(u'Имя:', self)
        firstnameLabel.move(50, 140)
        self.firstnameInput = QLineEdit(self)
        self.firstnameInput.move(170, 140)

        phoneLabel = QLabel(u'Телефон:', self)
        phoneLabel.move(50, 170)
        self.phoneInput = QLineEdit(self)
        self.phoneInput.move(170, 170)

        birthdateLabel = QLabel(u'Дата рождения:', self)
        birthdateLabel.move(50, 200)
        self.birthdateInput = QDateEdit(self)
        self.birthdateInput.setDisplayFormat('dd.MM.yyyy')
        self.birthdateInput.setDate(QDate.currentDate())
        self.birthdateInput.move(170, 200)

        registerButton = QPushButton(u'Зарегистрироваться', self)
        registerButton.move(50, 240)
        registerButton.clicked.connect(self.register_user)

        cancelButton = QPushButton(u'Отмена', self)
        cancelButton.move(50, 280)
        cancelButton.clicked.connect(self.cancel)

        self.show()

    def register_user(self):
        # считываем значения из полей ввода
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        confirm_password = self.confirmPasswordInput.text()
        lastname = self.lastnameInput.text()
        firstname = self.firstnameInput.text()
        phone = self.phoneInput.text()
        birthdate = self.birthdateInput.text()
        birthdate_obj = QDate.fromString(birthdate, "dd.MM.yyyy")
        birthdate_str = str(birthdate_obj.toString("yyyy-MM-dd"))
    
        # проверяем, что все поля заполнены
        if not username or not password or not confirm_password or not birthdate:
            QMessageBox.warning(self, u'Ошибка', u'Пожалуйста, заполните все поля')
            return
    
        # проверяем, что пароль и подтверждение пароля совпадают
        if password != confirm_password:
            QMessageBox.warning(self, u'Ошибка', u'Пароли не совпадают')
            return

        # создаем объект базы данных
        db = PhonebookDatabase()

        # проверяем, что пользователь с таким именем еще не зарегистрирован
        if db.check_duplicate(unicode(username).encode('utf-8')):
            QMessageBox.warning(self, u'Ошибка', u'Пользователь с таким именем уже зарегистрирован')
            return

        # добавляем нового пользователя в базу данных
        db.add_user(username, password)
        db.add_contact(firstname, lastname, phone, birthdate_str)
        # закрываем окно регистрации
        self.close()

    def cancel(self):
        # обработчик нажатия кнопки "Отмена"
        self.reject()


class MainWindow(QMainWindow):
    def __init__(self, login_window):
        print("MainWindow constructor called")
        super(MainWindow, self).__init__()

        self.login_window = login_window  # Store a reference to the LoginWindow instance

        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(300, 300, 700, 400)
        self.setWindowTitle(u'Phonebook')

        # создаем виджет с таблицей контактов
        contacts_widget = ContactsWidget(self)

        # добавляем виджет с таблицей контактов в layout главного окна
        layout = QVBoxLayout()
        layout.addWidget(contacts_widget)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def closeEvent(self, event):
        self.login_window.close()  # Close the LoginWindow instance when MainWindow is closed
        event.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    phonebook = Phonebook()
    sys.exit(app.exec_())
