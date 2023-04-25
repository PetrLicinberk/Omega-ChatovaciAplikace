import unittest

from src.server import db_connection, user


if __name__ == '__main__':
    unittest.main()


class UserTest(unittest.TestCase):
    def test_username_policy(self):
        u = user.User()
        self.assertRaises(user.InvalidLengthError, u.set_username, new_username='aa')
        self.assertRaises(user.InvalidLengthError, u.set_username, new_username='a' * 65)
        u.set_username('aaaaaa')
        self.assertEqual(u.get_username(), 'aaaaaa')
        self.assertRaises(user.InvalidCharactersError, u.set_username, new_username='aaa$')
        u.set_username('aaa')
        self.assertEqual(u.get_username(), 'aaa')

    def test_password_policy(self):
        u = user.User()
        self.assertRaises(user.InvalidLengthError, u.set_password, new_password='aa')
        self.assertRaises(user.InvalidLengthError, u.set_password, new_password='a' * 65)
        self.assertRaises(user.NoLowerCaseError, u.set_password, new_password='AAA')
        self.assertRaises(user.NoLowerCaseError, u.set_password, new_password='999')
        self.assertRaises(user.NoLowerCaseError, u.set_password, new_password='AA9')
        self.assertRaises(user.NoUpperCaseError, u.set_password, new_password='aaa')
        self.assertRaises(user.NoUpperCaseError, u.set_password, new_password='aa9')
        self.assertRaises(user.NoNumberError, u.set_password, 'aaA')
        u.set_password('Aa3')
        self.assertEqual(u.get_password(), user.hash_password('Aa3'))

    def test_get_user(self):
        db_conn = db_connection.get_instance()
        db_conn.address = '158.101.189.194'
        db_conn.user = 'app_test'
        db_conn.password = 'password'
        db_conn.name = 'chat_test'
        conn, cursor = db_connection.get_cursor()
        cursor.execute('delete from friend')
        cursor.execute('delete from message')
        cursor.execute('delete from user')
        cursor.execute('commit')
        cursor.close()
        conn.close()

        u = user.get_user_by_username('aaa')
        self.assertEqual(u, None)

        conn, cursor = db_connection.get_cursor()
        cursor.execute('insert into user(username, password) values(%s, %s)', ('aaa', 'bbb'))
        cursor.execute('commit')
        cursor.close()
        conn.close()

        u = user.get_user_by_username('aaa')
        self.assertNotEqual(u, None)
        self.assertEqual(u.get_username(), 'aaa')
        self.assertEqual(u.get_password(), None)

    def test_create_user(self):
        db_conn = db_connection.get_instance()
        db_conn.address = '158.101.189.194'
        db_conn.user = 'app_test'
        db_conn.password = 'password'
        db_conn.name = 'chat_test'
        conn, cursor = db_connection.get_cursor()
        cursor.execute('delete from friend')
        cursor.execute('delete from message')
        cursor.execute('delete from user')
        cursor.execute('commit')
        cursor.close()
        conn.close()
        u = user.User()
        u.set_username('aaa')
        u.set_password('Aa3')
        user.create_user(u)
        u2 = user.get_user_by_username('aaa')
        self.assertNotEqual(u2, None)
        self.assertEqual(u2.get_username(), 'aaa')

    def test_verify_login(self):
        db_conn = db_connection.get_instance()
        db_conn.address = '158.101.189.194'
        db_conn.user = 'app_test'
        db_conn.password = 'password'
        db_conn.name = 'chat_test'
        conn, cursor = db_connection.get_cursor()
        cursor.execute('delete from friend')
        cursor.execute('delete from message')
        cursor.execute('delete from user')
        cursor.execute('commit')
        cursor.close()
        conn.close()
        u = user.User()
        u.set_username('aaa')
        u.set_password('Aa3')
        user.create_user(u)

        u2, status = user.verify_login('bbb', 'Bb3')
        self.assertEqual(u2, None)
        self.assertEqual(status, 1)

        u2, status = user.verify_login('aaa', 'Bb3')
        self.assertEqual(u2, None)
        self.assertEqual(status, 1)

        u2, status = user.verify_login('aaa', 'Aa3')
        self.assertNotEqual(u2, None)
        self.assertEqual(u2.get_username(), u.get_username())
        self.assertEqual(u2.get_password(), u.get_password())
        self.assertEqual(status, 0)

    def test_exists(self):
        db_conn = db_connection.get_instance()
        db_conn.address = '158.101.189.194'
        db_conn.user = 'app_test'
        db_conn.password = 'password'
        db_conn.name = 'chat_test'
        conn, cursor = db_connection.get_cursor()
        cursor.execute('delete from friend')
        cursor.execute('delete from message')
        cursor.execute('delete from user')
        cursor.execute('commit')
        cursor.close()
        conn.close()

        u = user.User()
        u.set_username('aaa')
        u.set_password('Aa3')
        
        exists = user.does_exist(u)
        self.assertEqual(exists, False)

        user.create_user(u)

        exists = user.does_exist(u)
        self.assertEqual(exists, True)

    def test_update_details(self):
        db_conn = db_connection.get_instance()
        db_conn.address = '158.101.189.194'
        db_conn.user = 'app_test'
        db_conn.password = 'password'
        db_conn.name = 'chat_test'
        conn, cursor = db_connection.get_cursor()
        cursor.execute('delete from friend')
        cursor.execute('delete from message')
        cursor.execute('delete from user')
        cursor.execute('commit')
        cursor.close()
        conn.close()

        u = user.User()
        u.set_username('aaa')
        u.set_password('Aa3')
        user.create_user(u)
        u.update_details('Aaa', 'Bbb', 'Ccc')

        conn, cursor = db_connection.get_cursor()
        cursor.execute('select username, first_name, last_name, email \
                       from user where user.id = %s',
                       (u.get_id(),))
        details = cursor.fetchone()
        self.assertEqual(details[0], 'aaa')
        self.assertEqual(details[1], 'Aaa')
        self.assertEqual(details[2], 'Bbb')
        self.assertEqual(details[3], 'Ccc')
        cursor.close()
        conn.close()


    def test_get_user_details(self):
        db_conn = db_connection.get_instance()
        db_conn.address = '158.101.189.194'
        db_conn.user = 'app_test'
        db_conn.password = 'password'
        db_conn.name = 'chat_test'
        conn, cursor = db_connection.get_cursor()
        cursor.execute('delete from friend')
        cursor.execute('delete from message')
        cursor.execute('delete from user')
        cursor.execute('commit')
        cursor.close()
        conn.close()

        u = user.User()
        u.set_username('aaa')
        u.set_password('Aa3')
        user.create_user(u)
        u.update_details('Aaa', 'Bbb', 'Ccc')
        details = u.get_user_details()
        self.assertIn('username', details)
        self.assertEqual(details['username'], 'aaa')
        self.assertIn('first_name', details)
        self.assertEqual(details['first_name'], 'Aaa')
        self.assertIn('last_name', details)
        self.assertEqual(details['last_name'], 'Bbb')
        self.assertIn('email', details)
        self.assertEqual(details['email'], 'Ccc')

    def test_is_friend(self):
        db_conn = db_connection.get_instance()
        db_conn.address = '158.101.189.194'
        db_conn.user = 'app_test'
        db_conn.password = 'password'
        db_conn.name = 'chat_test'
        conn, cursor = db_connection.get_cursor()
        cursor.execute('delete from friend')
        cursor.execute('delete from message')
        cursor.execute('delete from user')
        cursor.execute('commit')
        cursor.close()
        conn.close()

        u1 = user.User()
        u1.set_username('aaa')
        u1.set_password('Aa3')
        user.create_user(u1)

        u2 = user.User()
        u2.set_username('bbb')
        u2.set_password('Bb3')
        user.create_user(u2)

        is_friend = u1.is_friend(u2.get_id())
        self.assertEqual(is_friend, False)

        conn, cursor = db_connection.get_cursor()
        cursor.execute('insert into friend(user_id, friend_id, accepted) \
                       values(%s, %s, %s)',
                       (u1.get_id(), u2.get_id(), True))
        cursor.execute('insert into friend(user_id, friend_id, accepted) \
                       values(%s, %s, %s)',
                       (u2.get_id(), u1.get_id(), True))
        cursor.execute('commit')
        cursor.close()
        conn.close()

        is_friend = u1.is_friend(u2.get_id())
        self.assertEqual(is_friend, True)

    def test_accept_friend_req(self):
        db_conn = db_connection.get_instance()
        db_conn.address = '158.101.189.194'
        db_conn.user = 'app_test'
        db_conn.password = 'password'
        db_conn.name = 'chat_test'
        conn, cursor = db_connection.get_cursor()
        cursor.execute('delete from friend')
        cursor.execute('delete from message')
        cursor.execute('delete from user')
        cursor.execute('commit')
        cursor.close()
        conn.close()

        u1 = user.User()
        u1.set_username('aaa')
        u1.set_password('Aa3')
        user.create_user(u1)

        u2 = user.User()
        u2.set_username('bbb')
        u2.set_password('Bb3')
        user.create_user(u2)

        u1.add_friend(u2._username)
        is_friend = u1.is_friend(u2.get_id())
        self.assertEqual(is_friend, False)
        is_friend = u2.is_friend(u1.get_id())
        self.assertEqual(is_friend, False)

        u2.accept_friend_req(u1.get_username())
        is_friend = u1.is_friend(u2.get_id())
        self.assertEqual(is_friend, True)
        is_friend = u2.is_friend(u1.get_id())
        self.assertEqual(is_friend, True)

    def test_decline_friend_req(self):
        db_conn = db_connection.get_instance()
        db_conn.address = '158.101.189.194'
        db_conn.user = 'app_test'
        db_conn.password = 'password'
        db_conn.name = 'chat_test'
        conn, cursor = db_connection.get_cursor()
        cursor.execute('delete from friend')
        cursor.execute('delete from message')
        cursor.execute('delete from user')
        cursor.execute('commit')
        cursor.close()
        conn.close()

        u1 = user.User()
        u1.set_username('aaa')
        u1.set_password('Aa3')
        user.create_user(u1)

        u2 = user.User()
        u2.set_username('bbb')
        u2.set_password('Bb3')
        user.create_user(u2)
        
        u1.add_friend(u2._username)
        u2.decline_friend_req(u1.get_username())
        is_friend = u1.is_friend(u2.get_id())
        self.assertEqual(is_friend, False)
        is_friend = u2.is_friend(u1.get_id())
        self.assertEqual(is_friend, False)

    def test_remove_friend(self):
        db_conn = db_connection.get_instance()
        db_conn.address = '158.101.189.194'
        db_conn.user = 'app_test'
        db_conn.password = 'password'
        db_conn.name = 'chat_test'
        conn, cursor = db_connection.get_cursor()
        cursor.execute('delete from friend')
        cursor.execute('delete from message')
        cursor.execute('delete from user')
        cursor.execute('commit')
        cursor.close()
        conn.close()

        u1 = user.User()
        u1.set_username('aaa')
        u1.set_password('Aa3')
        user.create_user(u1)

        u2 = user.User()
        u2.set_username('bbb')
        u2.set_password('Bb3')
        user.create_user(u2)
        
        u1.add_friend(u2._username)
        u2.accept_friend_req(u1.get_username())
        is_friend = u1.is_friend(u2.get_id())
        self.assertEqual(is_friend, True)
        is_friend = u2.is_friend(u1.get_id())
        self.assertEqual(is_friend, True)

        u1.remove_friend(u2.get_username())
        is_friend = u1.is_friend(u2.get_id())
        self.assertEqual(is_friend, False)
        is_friend = u2.is_friend(u1.get_id())
        self.assertEqual(is_friend, False)