# -*- coding: utf-8 -*-
import mysql.connector

from utils import encode_utf8


class PhonebookDatabase:
    def __init__(self):
        self.cnx = mysql.connector.connect(user='telephonebook', password='password',
                                           host='localhost',
                                           database='telephonebook')
        self.cursor = self.cnx.cursor()

    def __del__(self):
        self.cnx.close()

    def execute_query(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def execute_insert_query(self, query, values):
        self.cursor.execute(query, values)
        self.cnx.commit()

    def execute_update_query(self, query, values):
        self.cursor.execute(query, values)
        self.cnx.commit()

    def execute_delete_query(self, query, values):
        self.cursor.execute(query, values)
        self.cnx.commit()

    def get_contacts(self):
        query = ("SELECT * FROM contacts ORDER BY last_name")
        self.cursor.execute(query)
        columns = [col[0] for col in self.cursor.description]
        contacts = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return contacts

    def get_birthdays(self):
        query = ("SELECT * FROM contacts WHERE MONTH(birth_date) = MONTH(NOW()) "
                 "AND DAY(birth_date) BETWEEN DAY(NOW()) AND DAY(NOW()+7) ORDER BY DAY(birth_date)")
        return self.execute_query(query)

    def get_contact(self, contact_id):
        query = "SELECT * FROM contacts WHERE id = %s"
        result = self.execute_query(query, (contact_id,))
        print("Contact query result:", result)  # добавьте эту строку для вывода результатов запроса
        return result

    def add_contact(self, first_name, last_name, phone_number, birth_date):
        try:
            query = "INSERT INTO contacts (first_name, last_name, phone_number, birth_date) VALUES (%s, %s, %s, %s)"
            values = (first_name, last_name, phone_number, birth_date)
            encoded_values = encode_utf8(values)
            self.cursor.execute(query, encoded_values)
            self.cnx.commit()
            return True
        except mysql.connector.Error as error:
            print("Failed to insert contact: %s" % error)
            return False

    def update_contact(self, id, name, phone, email, birthday):
        query = "UPDATE contacts SET first_name=%s, last_name=%s, phone_number=%s, birth_date=%s WHERE id=%s"
        values = (name, phone, email, birthday, id)
        self.execute_update_query(query, values)

    def delete_contact(self, id):
        query = ("DELETE FROM contacts WHERE id=%s")
        values = (id,)
        self.execute_delete_query(query, values)

    def get_contacts_by_alphabet(self, first_letter, last_letter):
        query = (
            u"SELECT id, last_name, first_name, phone_number, birth_date "
            u"FROM contacts "
            u"WHERE last_name >= %s AND last_name <= %s "
            u"ORDER BY last_name"
        )
        self.cursor.execute(query, (first_letter, last_letter))
        return [
            {
                'id': row[0],
                'last_name': row[1],
                'first_name': row[2],
                'phone_number': row[3],
                'birth_date': row[4]
            }
            for row in self.cursor.fetchall()
        ]

    def check_duplicate(self, login):
        query = ("SELECT COUNT(*) FROM users WHERE login = %s")
        values = (login,)
        self.cursor.execute(query, values)
        count = self.cursor.fetchone()[0]
        return count > 0

    def add_user(self, login, password):
        try:
            query = "INSERT INTO users (login, password) VALUES (%s, %s)"
            # values = (unicode(login).encode('utf-8'), unicode(password).encode('utf-8'))
            values = (login, password)
            encoded_values = encode_utf8(values)
            self.cursor.execute(query, encoded_values)
            self.cnx.commit()
            return True
        except mysql.connector.Error as error:
            print("Failed to insert user: %s" % error)
            return False

    def check_login_password(self, login, password):
        query = ("SELECT COUNT(*) FROM users WHERE login = %s AND password = %s")
        values = (login, password)
        encoded_values = encode_utf8(values)
        self.cursor.execute(query, encoded_values)
        count = self.cursor.fetchone()[0]
        return count > 0
    

