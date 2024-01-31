from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import mysql.connector


class VigenereCipher(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        # Define DB
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Riya@2314",
            database="Cipher_db"
        )

        c = mydb.cursor()

        c.execute("CREATE DATABASE IF NOT EXISTS Cipher_db")

        mydb.commit()
        mydb.close()

        return Builder.load_file('Cipher.kv')

    message = ObjectProperty(None)
    key = ObjectProperty(None)

    def callback(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Riya@2314",
            database="Cipher_db"
        )
        c = mydb.cursor()
        #c.execute("CREATE TABLE users (name VARCHAR(255), password VARCHAR(255) , encrypted VARCHAR(255), user_id INTEGER AUTO_INCREMENT PRIMARY KEY)")
        #c.execute("SHOW TABLES")

        characters = "abcdefghijklmnopqrstuvwxyz"
        characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        characters += "1234567890"
        characters += " !@#$%^&*()-_+=`~;:'[]{}|<>,./?"
        characters += "\"\\"

        character_count = len(characters)

        def encrypt_character(plain, key):

            key_code = characters.index(key)
            plain_code = characters.index(plain)

            cipher_code = (key_code + plain_code) % character_count

            cipher = characters[cipher_code]

            return cipher

        def encrypt(plain, key):

            cipher = ""

            for (plain_index, plain_character) in enumerate(plain):
                key_index = plain_index % len(key)
                key_character = key[key_index]

                cipher_character = encrypt_character(key_character, plain_character)

                cipher += cipher_character

            return cipher

        def invert_character(character):

            character_code = characters.index(character)

            inverted_code = (character_count - character_code) % character_count
            inverted_character = characters[inverted_code]

            return inverted_character

        def invert(text):

            inverted_text = ""

            for character in text:
                inverted_text += invert_character(character)

            return inverted_text

        # def show_pass(username):

        for i in range(0, character_count):

            keytext = self.root.ids.username.text
            plaintext = self.root.ids.password.text

            encrypted = plaintext.startswith("!")

            if encrypted:
                plaintext = plaintext[1:]
                keytext = invert(keytext)

            ciphertext = encrypt(plaintext, keytext)

            if not encrypted:
                ciphertext = "!" + ciphertext

        self.root.ids.output.text = f'Encrypted Password: {ciphertext}'
        sql_command = "INSERT INTO users (name, password, encrypted) VALUES(%s, %s, %s)"
        values = (self.root.ids.username.text, self.root.ids.password.text, ciphertext)
        c.execute(sql_command, values)
        self.root.ids.password.text = ""
        self.root.ids.username.text = ""
        mydb.commit()
        mydb.close()

    def decrypt(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Riya@2314",
            database="Cipher_db"
        )
        c = mydb.cursor()

        keytext = self.root.ids.username1.text
        sql_command = "SELECT * FROM `users` WHERE `name` = %s"
        key = (keytext,)

        try:

            c.execute(sql_command, key)
            result = c.fetchall()

            for i in result:
                pwd = i[1]
            self.root.ids.output1.text = f'Your password is: {pwd}'


        except:
            self.root.ids.output1.text = f'Please enter valid username'

        self.root.ids.username1.text = ""
        mydb.commit()
        mydb.close()


VigenereCipher().run()