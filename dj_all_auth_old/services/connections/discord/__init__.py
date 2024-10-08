from .Discord import Discord


def unlink(user):
    revoke_token(user)


def refresh_token(user):
    discord = Discord()
    discord.refresh_token(user)


def revoke_token(user):
    discord = Discord()
    discord.revoke_token(user)
