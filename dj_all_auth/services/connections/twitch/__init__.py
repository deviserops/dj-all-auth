from .Twitch import Twitch


def unlink(user):
    revoke_token(user)


def refresh_token(user):
    twitch = Twitch()
    twitch.refresh_token(user)


def revoke_token(user):
    twitch = Twitch()
    twitch.revoke_token(user)
