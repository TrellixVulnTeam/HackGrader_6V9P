import sys
import unittest
import os
import solution
from solution import Client


from faker import Factory
fakerr = Factory.create()


sys.path.append("..")


class SqlManagerTests(unittest.TestCase):

    def setUp(self):
        solution.create_clients_table()
        solution.register('Tester', '123')

    def tearDown(self):
        solution.cursor.execute('DROP TABLE clients')

    @classmethod
    def tearDownClass(cls):
        os.remove("bank.db")

    def test_register(self):
        solution.register('Dinko', '123123')

        solution.cursor.execute('SELECT Count(*)  FROM clients WHERE username = (?) AND password = (?)', ('Dinko', '123123'))
        users_count = solution.cursor.fetchone()

        self.assertEqual(users_count[0], 1)

    def test_login(self):
        logged_user = solution.login('Tester', '123')
        self.assertEqual(logged_user.get_username(), 'Tester')

    def test_login_wrong_password(self):
        logged_user = solution.login('Tester', '123567')
        self.assertFalse(logged_user)

    def test_change_message(self):
        logged_user = solution.login('Tester', '123')
        new_message = "podaivinototam"
        solution.change_message(new_message, logged_user)
        self.assertEqual(logged_user.get_message(), new_message)

    def test_change_password(self):
        logged_user = solution.login('Tester', '123')
        new_password = "12345"
        solution.change_pass(new_password, logged_user)

        logged_user_new_password = solution.login('Tester', new_password)
        self.assertEqual(logged_user_new_password.get_username(), 'Tester')


class ClientTests(unittest.TestCase):

    def setUp(self):
        self.test_client = Client(1, "Ivo", 200000.00, "Bitcoin mining makes me rich")

    def test_client_id(self):
        self.assertEqual(self.test_client.get_id(), 1)

    def test_client_name(self):
        self.assertEqual(self.test_client.get_username(), "Ivo")

    def test_client_balance(self):
        self.assertEqual(self.test_client.get_balance(), 200000.00)

    def test_client_message(self):
        self.assertEqual(self.test_client.get_message(), "Bitcoin mining makes me rich")


class TestRequirements(unittest.TestCase):

    def test_faker_is_installed(self):
        self.assertIsNotNone(fakerr.word())


if __name__ == '__main__':
    unittest.main()
