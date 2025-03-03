from database import DatabaseCRUD
from abc import ABC, abstractmethod

class IUsers(ABC):
    @abstractmethod
    def get_user_data(self):
        pass

    @abstractmethod
    def add_user(self):
        pass

    @abstractmethod
    def update_user(self):
        pass

    @abstractmethod
    def delete_user(self):
        pass

class Users(IUsers):
    def __init__(self, UserID=None, FirstName=None, LastName=None, Email=None, PasswordHash=None, UserType=None):
        self.__UserID = UserID
        self.__FirstName = FirstName
        self.__LastName = LastName
        self.__Email = Email
        self.__PasswordHash = PasswordHash
        self.__UserType = UserType

    def get_user_data(self):
        dbconn = DatabaseCRUD()
        cond = ["UserID=" + str(self.__UserID)] if self.__UserID else ["1=1"]
        user_data = dbconn.DBRead(tbl='Users', sfld='*', scond=cond)
        return user_data

    def add_user(self):
        dbconn = DatabaseCRUD()
        dbconn.DBCreate(tbl='Users', sidName='UserID', sfld='FirstName, LastName, Email, PasswordHash, UserType',
                        svalue=f"'{self.__FirstName}', '{self.__LastName}', '{self.__Email}', '{self.__PasswordHash}', '{self.__UserType}'")

    def update_user(self):
        dbconn = DatabaseCRUD()
        cond = ["UserID=" + str(self.__UserID)]
        sfld = f"FirstName='{self.__FirstName}', LastName='{self.__LastName}', Email='{self.__Email}', PasswordHash='{self.__PasswordHash}', UserType='{self.__UserType}'"
        dbconn.DBUpdate(tbl='Users', sfld=sfld, scond=cond)

    def delete_user(self):
        dbconn = DatabaseCRUD()
        cond = ["UserID=" + str(self.__UserID)]
        dbconn.DBDelete(tbl='Users', scond=cond)
        
        