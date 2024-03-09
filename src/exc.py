from fastapi import HTTPException


class ApiKeyDontFind(HTTPException):
    def __init__(self):
        self.text = "You are not registered"


class UserDontFind(HTTPException):
    def __init__(self):
        self.text = "User don't find"


class TweetDontFind(HTTPException):
    def __init__(self):
        self.text = "Message don't find"


class FileDontSave(HTTPException):
    def __init__(self):
        self.text = "File don't save"


class MaxSizeFile(HTTPException):
    def __init__(self):
        self.text = "Very big file"
