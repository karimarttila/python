from hashlib import md5
from simpleserver.util.consts import ENTER, EXIT
from simpleserver.util.logger import SSLogger

# Run this in Console to refresh module in console:
# runfile('/mnt/edata/aw/kari/github/python/webstore-demo/simple-server/simpleserver/userdb/users.py',
#     wdir='/mnt/edata/aw/kari/github/python/webstore-demo/simple-server')


class Users:
    """Users class."""

    myLogger = SSLogger(__name__).get_logger()
    counter = None

    # Simulates initial database.
    users = {
        1: {
            'userid': '1',
            'email': 'kari.karttinen@foo.com',
            'first_name': 'Kari',
            'last_name': 'Karttinen',
            'hashed_password': '87ee0597c41d7ab8c074d7dc4794716d'
        },
        2: {
            'userid': '2',
            'email': 'timo.tillinen@foo.com',
            'first_name': 'Timo',
            'last_name': 'Tillinen',
            'hashed_password': 'ee5f0c6f4d191b58497f7db5c5c9caf8'
        },
        3: {
            'userid': '3',
            'email': 'erkka.erkkila@foo.com',
            'first_name': 'Erkka',
            'last_name': 'Erkkilä',
            'hashed_password': '8f0e3b40464dff73c392dce9f2dce9dd'
        }
    }

    @staticmethod
    def __create_counter():
        """Creates counter for the module.
        Also a Python closure example."""
        counter = 3  # Initial value of users.

        def add_one():
            nonlocal counter
            counter = counter + 1
            return counter
        return add_one

    def email_already_exists(self, given_email):
        """Checks if user email already exists in the user db: exists: True, False otherwise."""
        self.myLogger.debug(ENTER)
        candidates = list(filter((lambda x: x['email'] == given_email), self.users.values()))
        ret = (len(candidates) > 0)
        self.myLogger.debug(EXIT)
        return ret

    def add_user(self, new_email, first_name, last_name, password):
        """Adds new user to the user db. ret=ok, if success, ret=failed otherwise."""
        self.myLogger.debug(ENTER)
        if not self.email_already_exists(new_email):
            new_user = {}
            new_id = self.counter()
            new_str_id = str(new_id)
            hashed_password = md5(password.encode('utf-8')).hexdigest()
            new_user['userid'] = new_str_id
            new_user['email'] = new_email
            new_user['first_name'] = first_name
            new_user['last_name'] = last_name
            new_user['hashed_password'] = hashed_password
            self.users[new_id] = new_user
            ret = {'email': new_email, 'ret': 'ok'}
        else:
            self.myLogger.warning('Failure: email already exists: ' + new_email)
            ret = {'email': new_email, 'ret': 'failed', 'msg': 'Email already exists'}
        self.myLogger.debug(EXIT)
        return ret

    def check_credentials(self, user_email, user_password):
        """Checks user credentials in the user db."""
        self.myLogger.debug(ENTER)
        ret = False
        hashed_password = md5(user_password.encode('utf-8')).hexdigest()
        candidates = list(filter((lambda x: (x['email'] == user_email)
                                            and (x['hashed_password'] == hashed_password)), self.users.values()))
        if candidates is None:
            self.myLogger.error("lambda returned None")
        elif len(candidates) == 1:  # Normal scenario: found one.
            ret = True
        elif len(candidates) == 0:  # Normal scenario: found none.
            pass
        else:
            self.myLogger.error("lambda returned something else than 0 or 1 user")
        self.myLogger.debug(EXIT)
        return ret

    def __init__(self):
        self.counter = self.__create_counter()
        pass
