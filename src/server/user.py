import re
import hashlib
import src.server.db_connection as db
import datetime

class User:
    def __init__(self):
        self._id: int = 0
        self._username: str = None
        self._password: str = None

    def get_id(self):
        '''
        Returns user id.

        :return: user id
        '''
        return self._id

    def get_username(self) -> str:
        '''
        Returns user's username.
        :return: username
        '''
        return self._username
    def set_username(self, new_username: str):
        '''
        Checks if the new username is 3 - 64 characters long
        and contains only allowed characters.
        Sets the username.
        '''
        if len(new_username) < 3 or len(new_username) > 64:
            raise InvalidLengthError
        if re.search(r'^[a-z0-9_-]*$', new_username, re.IGNORECASE) is None:
            raise InvalidCharactersError
        self._username = new_username

    def get_password(self) -> str:
        '''
        Returns password hash

        :return: password
        '''
        return self._password
    def set_password(self, new_password):
        '''
        Checks if the password is 3 - 64 characters long
        and contains at least one lower case character,
        one upper case letter and one number.
        '''
        if len(new_password) < 3 or len(new_password) > 64:
            raise InvalidLengthError
        if re.search(r'[a-z]', new_password) is None:
            raise NoLowerCaseError
        if re.search(r'[A-Z]', new_password) is None:
            raise NoUpperCaseError
        if re.search(r'[0-9]', new_password) is None:
            raise NoNumberError
        self._password = hash_password(new_password)

    def save(self):
        '''
        Saves the user to the database.
        '''
        if self._id == 0:
            create_user(self)
        else:
            update_user(self)

    def get_user_details(self):
        '''
        Gets userdetails from the database.

        :return: user details dictionary
        '''
        connection, cursor = db.get_cursor()
        cursor.execute('select username, first_name, last_name, email \
                       from user where user.id = %s',
                       (self._id,))
        user = cursor.fetchone()
        user_details = {}
        user_details['username'] = user[0]
        user_details['first_name'] = user[1]
        user_details['last_name'] = user[2]
        user_details['email'] = user[3]
        return user_details


    def get_friend_list(self):
        '''
        Gets list of friends from the database.

        :return: list of friends
        '''
        connection, cursor = db.get_cursor()
        cursor.execute('select u.username \
                       from friend f inner join user u on f.friend_id = u.id \
                       where f.user_id = %s and f.accepted = true \
                       and exists (select accepted from friend where friend.user_id = u.id and friend.accepted = true)', (self._id, ))
        friends = []
        for (username,) in cursor:
            friends.append(username)
        connection.close()
        return friends
    
    def add_friend(self, username: str):
        '''
        Adds new friend request to the database.

        :param username: friend username 
        '''
        connection, cursor = db.get_cursor()
        cursor.execute('select user.id \
                       from friend inner join user on friend.friend_id = user.id \
                       where friend.user_id = %s and user.username = %s',
                       (self._id, username))
        results = []
        for (friend_id,) in cursor:
            results.append(friend_id)
        is_friend = len(results) > 0
        if not is_friend:
            cursor.execute('select id \
                   from user where user.username = %s', (username,))
            results = []
            for (id,) in cursor:
                results.append(id)
            cursor.execute('insert into friend(user_id, friend_id, accepted) \
                           values(%s, %s, true)',
                           (self._id, results[0]))
            cursor.execute('insert into friend(user_id, friend_id, accepted) \
                           values(%s, %s, false)',
                           (results[0], self._id))
            cursor.execute('commit')
        connection.close()

    def remove_friend(self, username: str):
        '''
        Removes friend from friend list and deletes all messages.

        :param username: friend username
        '''
        connection, cursor = db.get_cursor()
        cursor.execute('select user.id \
                       from friend inner join user on friend.friend_id = user.id \
                       where friend.user_id = %s and user.username = %s',
                       (self._id, username))
        results = []
        for (friend_id,) in cursor:
            results.append(friend_id)
        is_friend = len(results) > 0
        if is_friend:
            cursor.execute('delete from friend \
                        where friend.user_id = %s and friend.friend_id = %s',
                        (self.get_id(), results[0]))
            cursor.execute('delete from friend \
                        where friend.user_id = %s and friend.friend_id = %s',
                        (results[0], self.get_id()))
            cursor.execute('delete from message \
                           where from_user_id = %s and to_user_id = %s',
                           (self.get_id(), results[0]))
            cursor.execute('delete from message \
                           where from_user_id = %s and to_user_id = %s',
                           (results[0], self.get_id()))
            cursor.execute('commit')

    def get_friend_req(self):
        '''
        Gets all friend requests from the database.

        :return: list of friend requests.
        '''
        connection, cursor = db.get_cursor()
        cursor.execute('select username \
                       from friend inner join user on friend.friend_id = user.id \
                       where friend.user_id = %s and accepted = false',
                       (self._id,))
        results = []
        for (username,) in cursor:
            results.append(username)
        return results

    def accept_friend_req(self, username: str):
        '''
        Accepts friends request.

        :param username: friend username
        '''
        connection, cursor = db.get_cursor()
        cursor.execute('select id \
                   from user where user.username = %s', (username,))
        friend_id = []
        for (id,) in cursor:
            friend_id.append(id)
        if len(friend_id) > 0:
            cursor.execute('update friend \
                       set accepted = true \
                       where friend.user_id = %s and friend.friend_id = %s', 
                       (self._id, friend_id[0]))
            cursor.execute('commit')

    def decline_friend_req(self, username: str):
        '''
        Declines friend request.

        :param username: friend username
        '''
        connection, cursor = db.get_cursor()
        cursor.execute('select id \
                   from user where user.username = %s', (username,))
        friend_id = []
        for (id,) in cursor:
            friend_id.append(id)
        if len(friend_id) > 0:
            cursor.execute('delete from friend \
                           where friend.user_id = %s and friend.friend_id = %s', 
                       (self._id, friend_id[0]))
            cursor.execute('delete from friend \
                           where friend.user_id = %s and friend.friend_id = %s', 
                       (friend_id[0], self._id))
            cursor.execute('commit')
    
    def is_friend(self, friend_id):
        '''
        Checks wether the two user are friends.

        :param friend_id: friend id
        :retrun: True if they are otherwise False
        '''
        connection, cursor = db.get_cursor()
        cursor.execute('select id \
                       from friend \
                       where friend.friend_id = %s and friend.user_id = %s and accepted = true \
                       and exists (select accepted from friend f where f.user_id = friend.friend_id and f.friend_id = friend.user_id and f.accepted = true)',
                       (self._id, friend_id))
        results = []
        for (id,) in cursor:
            results.append(id)
        connection.close()
        return len(results) > 0
    
    def update_details(self, first_name, last_name, email):
        '''
        Updates user details.

        :param first_name: new first name
        :param last_name: new last name
        :param email: new email
        '''
        connection, cursor = db.get_cursor()
        cursor.execute('update user \
                       set first_name = %s, \
                       last_name = %s, \
                       email = %s \
                       where id = %s',
                       (first_name, last_name, email, self._id))
        cursor.execute('commit')


def get_user_by_username(username: str) -> User:
    '''
    Finds user by username in the database.

    :return: User instance
    '''
    connection, cursor = db.get_cursor()
    cursor.execute('select id, username \
                   from user where user.username = %s', (username,))
    users = []
    for (id, name) in cursor:
        user = User()
        user._id = id
        user.set_username(name)
        users.append(user)
    connection.close()
    if len(users) == 0:
        return None
    else:
        return users[0]
    
def get_all_users_by_name(username: str, user: User):
    '''
    Find all users with similar name in the database.

    :param username: username
    '''
    connection, cursor = db.get_cursor()
    name = '%{name}%'.format(name=username)
    cursor.execute('select id, username \
                   from user u \
                   where username like %s \
                   and not exists(select id from friend \
                   where friend.friend_id = u.id and friend.user_id = %s)',
                   (name, user.get_id()))
    users = []
    for (id, username) in cursor:
        if username != user.get_username():
            users.append(username)
    connection.close()
    return users

def create_user(user: User):
    '''
    Creates new user and seve it to database.

    :param user: user to be saved to the database
    '''
    connection, cursor = db.get_cursor()
    cursor.execute('insert into user(username, password) values(%s, %s)', (user._username, user._password))
    user._id = cursor.lastrowid
    cursor.execute('commit')

def delete_user(user: User):
    '''
    Deletes a user from the database and deletes all his messages and friend list

    :param user: user to be deleted
    '''
    connection, cursor = db.get_cursor()
    cursor.execute('delete from message \
                   where from_user_id = %s', (user.get_id(),))
    cursor.execute('delete from message \
                   where to_user_id = %s', (user.get_id(),))
    cursor.execute('delete from friend \
                   where user_id = %s', (user.get_id(),))
    cursor.execute('delete from friend \
                   where friend_id = %s', (user.get_id(),))
    cursor.execute('delete from user \
                   where id = %s', (user.get_id(),))
    cursor.execute('commit')

def update_user(user: User):
    '''
    Updates the username and password in the database.

    :param user: user to be updated
    '''
    connection, cursor = db.get_cursor()
    cursor.execute('update user set username = %s, password = %s where id = %s', (user._username, user._password))
    cursor.execute('commit')

def does_exist(user: User):
    '''
    Checks if the user exists in the database.

    :param user: user to be checked
    '''
    connection, cursor = db.get_cursor()
    cursor.execute('select id from user where username = %s', (user.get_username(), ))
    result = cursor.fetchall()
    return len(result) > 0

def verify_login(username: str, password: str):
    '''
    Verifys username and password.

    :return: User instance if correct otherwise None
    '''
    connection, cursor = db.get_cursor()
    cursor.execute('select * from user where username = %s', (username, ))
    users = cursor.fetchall()
    if len(users) == 0:
        return None, 1
    if users[0][2] != hash_password(password):
        return None, 1
    user = User()
    user._id = users[0][0]
    user._username = users[0][1]
    user._password = users[0][2]
    return user, 0


class Message:
    def __init__(self) -> None:
        self._id = None
        self._from = None
        self._to = None
        self._content = None
        self._date = None

    def get_id(self) -> int:
        '''
        :return: message id
        '''
        return self._id
    def get_from(self) -> str:
        '''
        :return: username who sent the message
        '''
        return self._from
    def get_to(self) -> str:
        '''
        :return: username who recieved the message
        '''
        return self._to
    def get_content(self) -> str:
        '''
        :return: message content
        '''
        return self._content
    def get_date(self) -> str:
        '''
        :return: datetime when the message was sent
        '''
        return self._date.strftime('%d-%m-%Y %H:%M')


def hash_password(password: str):
    '''
    Hashes the given password.

    :param password: password to be hashed

    :return: password hash
    '''
    alg = hashlib.sha512()
    alg.update(bytes(password, 'utf-8'))
    hash = alg.hexdigest()
    return hash

def send_message(from_user: User, to_user: User, content: str):
    '''
    Saves new message to the database.

    :param from_user: who sent the message
    :param to_user: who recieved message
    :param content: message content 
    '''
    connection, cursor = db.get_cursor()
    cursor.execute('insert into message(from_user_id, to_user_id, content, date) \
                   values(%s, %s, %s, sysdate())',
                   (from_user.get_id(), to_user.get_id(), content))
    cursor.execute('commit')

def get_messages(user1: User, user2: User):
    '''
    Retrieves messages from the database.

    :param user1: user
    :param user2: friend

    :return: list of messages
    '''
    connection, cursor = db.get_cursor()
    cursor.execute('select m.id, f.username , t.username, m.content, m.date \
                   from message m inner join user f on m.from_user_id = f.id \
                   inner join user t on m.to_user_id = t.id \
                   where f.id = %s and t.id = %s or f.id = %s and t.id = %s \
                   order by m.id',
                   (user1.get_id(), user2.get_id(), user2.get_id(), user1.get_id()))
    messages = []
    for (id, from_user, to_user, content, date) in cursor:
        message = Message()
        message._id = id
        message._from = from_user
        message._to = to_user
        message._content = content
        message._date = date
        messages.append(message)
    return messages

class InvalidLengthError(Exception):
    pass
class InvalidCharactersError(Exception):
    pass
class NoLowerCaseError(Exception):
    pass
class NoUpperCaseError(Exception):
    pass
class NoNumberError(Exception):
    pass