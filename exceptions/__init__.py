"""
Discord bot for GBF crew Luminosity. Author: Anton#9396
Parts of code borrowed from Krypton's bot template: https://github.com/kkrypt0nn
"""


class UserBlacklisted(Exception):
    """
    Thrown when a user is attempting something, but is blacklisted.
    """

    def __init__(self, message="User is blacklisted!"):
        self.message = message
        super().__init__(self.message)


class UserNotOwner(Exception):
    """
    Thrown when a user is attempting something, but is not an owner of the bot.
    """

    def __init__(self, message="User is not an owner of the bot!"):
        self.message = message
        super().__init__(self.message)

class UserNotCrew(Exception):
    """
    Thrown when a user is attempting something, but is not a crew member.
    """

    def __init__(self, message="User is not an crew member!"):
        self.message = message
        super().__init__(self.message)