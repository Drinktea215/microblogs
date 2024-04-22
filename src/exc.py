from fastapi import HTTPException


class ApiKeyDontFind(HTTPException):
    def __init__(self):
        self.text = "You are not registered"
        self.type = "ApiKeyDontFind"


class UserDontFind(HTTPException):
    def __init__(self):
        self.text = "User don't find on id"
        self.type = "UserDontFind"


class TweetDontFind(HTTPException):
    def __init__(self):
        self.text = "Message don't find"
        self.type = "TweetDontFind"


class LikeIsExist(HTTPException):
    def __init__(self):
        self.text = "Like is exist"
        self.type = "LikeIsExist"


class LikeDoesntExist(HTTPException):
    def __init__(self):
        self.text = "Like doesn't exist"
        self.type = "LikeDoesntExist"


class FileDontSave(HTTPException):
    def __init__(self):
        self.text = "File don't save"
        self.type = "FileDontSave"


class MaxSizeFile(HTTPException):
    def __init__(self):
        self.text = "Very big file. The file must not exceed 5 Mb."
        self.type = "MaxSizeFile"
