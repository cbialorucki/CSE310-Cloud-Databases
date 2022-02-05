from fileinput import filename
from datetime import datetime
import enum, re, firebase_admin, const
from firebase_admin import credentials
from firebase_admin import firestore

class DB:
    """A cloud database to demonstrate a login system."""
    
    class UserAttribute(enum.Enum):
        """An enum used to describe different acceptable user attributes."""
        ID = 0
        Name = 1
        Phone = 2
        Email = 3
        Password = 4


    def __init__(self):
        cred = credentials.Certificate("D:\Downloads\cse-310-cloud-databases-217b0a528443.json")
        firebase_admin.initialize_app(cred)

        self._db = firestore.client()

    def AddUser(self, Name, Phone, Email, Password):
        """Adds a user account to the current database.

        :param Name str: The name of the new user.
        :param Phone str: The phone number of the new user.
        :param Email str: The email address of the new user.
        :param Password str: The password the new user selected for their account.
        :returns: bool: True if the account creation was successful, False if it was unsuccessful.

        """
        Email = Email.lower()
        if self.FindUser(self.UserAttribute.Phone, Phone) or self.FindUser(self.UserAttribute.Email, Email):
            return False
        self._db.collection(const.USER_TABLE_NAME).add({'Name': Name, 'Phone': Phone, 'Email': Email, 'Password': Password})
        return True

    def FindUser(self, UserAttribute, Input):
        """Finds a user account for a given input.

        :param UserAttribute UserAttribute: The user attribute to use for searching for the user.
        :param Input str: The string used to search for the user according to the UserAttribute.
        :returns: list[str]: A dictionary containing the Name, Phone, and Email Address of the found user.

        """
        if UserAttribute == self.UserAttribute.Name:
            try:
                return self._db.collection(const.USER_TABLE_NAME).where("Name", "==", Input).get()
            except IndexError:
                return False
        elif UserAttribute == self.UserAttribute.Phone:
            try:
                return self._db.collection(const.USER_TABLE_NAME).where("Phone", "==", Input).get()[0]
            except IndexError:
                return False
        elif UserAttribute == self.UserAttribute.Email:
            try:
                return self._db.collection(const.USER_TABLE_NAME).where("Email", "==", Input).get()[0]
            except IndexError:
                return False
        elif UserAttribute == self.UserAttribute.ID:
            try:
                return self._db.collection(const.USER_TABLE_NAME).document(Input).get()
            except IndexError:
                return False
        return False

    def DoesUserExist(self, Email):
        """Finds if a user account exists.

        :param Email str: The email address for the user account.
        :returns: bool: True if the user account exists in the database, False if the user account does not.

        """
        if self.FindUser(self.UserAttribute.Email, Email):
            return True
        return False

    def AttemptLogIn(self, Email, Password):
        """Attempts to log in the user.

        :param Email str: The email address for the user account.
        :param Password str: The password used to try logging in.
        :returns: str: The user account ID if the log in was successful, False if the user account does not.

        """
        User = self.FindUser(self.UserAttribute.Email, Email)
        if User:
            if self._DoesPasswordMatch(User.id, Password):
                return User.id
        return False
    
    def GetEmailAddress(self, UserID):
        """Gets the email address for a specified user.

        :param UserID: The UserID for the user account to get the email address from.
        :returns: str: The user's email address if the UserID was valid, False if the UserID was invalid.

        """
        try:
            return self.FindUser(self.UserAttribute.ID, UserID).to_dict()['Email']
        except IndexError:
            return False

    def GetName(self, UserID):
        """Gets the name for a specified user.

        :param UserID: The UserID for the user account to get the email address from.
        :returns: str: The user's name if the UserID was valid, False if the UserID was invalid.

        """
        try:
            return self.FindUser(self.UserAttribute.ID, UserID).to_dict()['Name']
        except IndexError:
            return False
    
    def GetPhoneNumber(self, UserID):
        """Gets the phone number for a specified user.

        :param UserID: The UserID for the user account to get the email address from.
        :returns: str: The user's phone number if the UserID was valid, False if the UserID was invalid.

        """
        try:
            return self.FindUser(self.UserAttribute.ID, UserID).to_dict()['Phone']
        except IndexError:
            return False

    def _DoesPasswordMatch(self, UserID, Password):
        """Notifies if a password matches for a specified user.

        :param UserID str: The ID for the user account to test if the password matches.
        :param Password str: The password used to try matching it.
        :returns: bool: True if the password was correct, False if the password was not.

        """
        CorrectPassword = self.FindUser(self.UserAttribute.ID, UserID).to_dict()['Password']
        return Password == CorrectPassword

    def DeleteUser(self, UserID, Password):
        """Deletes a specified user.

        :param Email str: The email address of the user account to delete.
        :param Password str: The password used for the user account.
        :returns: bool: True if the account deletion was successful, False if it was not.

        """
        if self._DoesPasswordMatch(UserID, Password):
            self._db.collection(const.USER_TABLE_NAME).document(UserID).delete()
            return True
        return False
    
    def ChangeUserAttribute(self, UserID, UserAttribute, Value, Password):
        """Changes an attribute about a user.

        :param UserID str: The user ID for the user account.
        :param UserAttribute UserAttribute: The attribute to change about the user account.
        :param Value str: The new value for the specified attribute.
        :param Password str: The password used for the user account.
        :returns: bool: True if the change was successful, False if the user account does not.

        """
        Value = Value.strip()
        if self._DoesPasswordMatch(UserID, Password):
            if UserAttribute == self.UserAttribute.Email and self.IsEmailValid(Value):
                self._db.collection(const.USER_TABLE_NAME).document(UserID).update({"Email": self.IsEmailValid(Value)})
            elif UserAttribute == self.UserAttribute.Name:
                self._db.collection(const.USER_TABLE_NAME).document(UserID).update({"Name": Value})
            elif UserAttribute == self.UserAttribute.Phone and self.IsPhoneValid(Value):
                self._db.collection(const.USER_TABLE_NAME).document(UserID).update({"Phone": self.IsPhoneValid(Value)})
            elif UserAttribute == self.UserAttribute.Password:
                self._db.collection(const.USER_TABLE_NAME).document(UserID).update({"Password": Value})
            else: 
                return False
            return True
        return False
    
    @staticmethod
    def IsEmailValid(Email):
        """Determines if an Email address is valid.
        
        :param Email str: The email address to validate.
        :returns: str: The validated email address if valid, False if the provided email address was invalid.
        
        """
        Email = Email.lower()
        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', Email):
            return Email
        return False

    @staticmethod
    def IsPhoneValid(Phone):
        """Determines if a phone number is valid.
        
        :param Phone str: The phone number to validate.
        :returns: str: The validated phone number if valid, False if the provided phone number was invalid.
        
        """
        SanitizedValue = re.sub('[^0-9]','', Phone)
        if len(SanitizedValue) == 10:
            return SanitizedValue
        return False
    

