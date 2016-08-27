import uuid

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
from src.models.alerts.alert import Alert
import src.models.users.constants as UserConstants


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an email/password combo sent by the form is valid or not
        Checks that the email exists and that the password associated to that email is correct

        :param str email: The user's email
        :param str password: A sha512 hashed password
        :return: True if valid, False otherwise
        """

        user_data = Database.find_one(UserConstants.COLLECTION, {'email': email}) #Password is in sha512 -> pbkdf2_sha512
        if user_data is None:
            # Tell the user their email does not exist
            raise UserErrors.UserNotExistsError("Your user does not exists")

        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was wrong")

        return True

    @staticmethod
    def register_user(email, password):
        """Registers a user with form.email and form.password (sha-512)

        :param email: user's email
        :param password: sha512-hashed password
        :return: true if success, false
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {'email': email})
        if user_data is not None:
            # Already registered user
            raise UserErrors.UserAlreadyRegisteredError("Already Registered")
            pass

        if not Utils.email_is_valid(email):
            # Tell the user the email is not correct
            raise UserErrors.InvalidEmailError("Invalid Email Format")
            pass

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def find_by_email(cls, email):
        data = Database.find_one(UserConstants.COLLECTION, {'email': email})
        return cls(**data)

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
