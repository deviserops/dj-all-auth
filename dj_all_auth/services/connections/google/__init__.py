from .Google import Google


def unlink(user):
    revoke_token(user)


def refresh_token(user):
    google = Google()
    google.refresh_token(user)


def revoke_token(user):
    google = Google()
    google.revoke_token(user)
