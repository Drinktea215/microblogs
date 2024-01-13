class ApiKeyDontFind(Exception):
    def __init__(self):
        self.text = "You are not registered"


class UserDontFind(Exception):
    def __init__(self):
        self.text = "User don't find"


class TweetDontFind(Exception):
    def __init__(self):
        self.text = "Message don't find"


class FileDontSave(Exception):
    def __init__(self):
        self.text = "File don't save"


class MaxSizeFile(Exception):
    def __init__(self):
        self.text = "Very big file"
