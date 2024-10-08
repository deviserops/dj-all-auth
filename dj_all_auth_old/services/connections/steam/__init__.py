from .Steam import Steam


def unlink(user):
    steam = Steam()
    steam.revoke(user)
