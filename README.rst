===============
DJ All Auth
===============

``Django all auth`` includes all account, including django default, OAuth (Google, Discord, Twitch), openId (Steam).

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "account" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        'dj_all_auth',
    ]

2. Include the polls URLconf in your project urls.py like this::

    # if you are not using /accounts url then you need to add `LOGIN_URL = '<your-url>'` in your settings.py

    path('accounts/', include('dj_all_auth.urls')),


3. Add context processor to settings.py::

    'dj_all_auth.context_processors.__config'


4. Add dj_all_auth settings to settings.py::

    DJ_ALL_AUTH = {
        # static path of logo image
        'LOGO': None,
        'CONNECTIONS': {
            # name of the url that will be used once OAuth is completed
            'REDIRECT_URI_NAME': None,
            'GOOGLE': {
                # Set {domain-with-above-url-without-locale (en/gb)}/accounts/google/authenticated to twitch redirect url
                'CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID') if os.getenv('GOOGLE_CLIENT_ID') else None,
                'CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET') if os.getenv('GOOGLE_CLIENT_SECRET') else None,
                'SCOPE': ['openid', 'email', 'https://www.googleapis.com/auth/drive.file']
            },
            'TWITCH': {
                # Set {domain-with-above-url-without-locale (en/gb)}/account/twitch/authenticated to twitch redirect url
                'CLIENT_ID': os.getenv('TWITCH_CLIENT_ID') if os.getenv('TWITCH_CLIENT_ID') else None,
                'CLIENT_SECRET': os.getenv('TWITCH_CLIENT_SECRET') if os.getenv('TWITCH_CLIENT_SECRET') else None,
                'SCOPE': ['openid', 'user:read:email', 'user:read:broadcast']
            },
            'DISCORD': {
                # Set {domain-with-above-url-without-locale (en/gb)}/account/discord/authenticated to discord redirect url
                'CLIENT_ID': os.getenv('DISCORD_CLIENT_ID') if os.getenv('DISCORD_CLIENT_ID') else None,
                'CLIENT_SECRET': os.getenv('DISCORD_CLIENT_SECRET') if os.getenv('DISCORD_CLIENT_SECRET') else None,
                'SCOPE': ['identify', 'email', 'connections', 'guilds', 'guilds.join']
            }
        }
    }

4. To create models run::

    python manage.py migrate

5. If you are using multilanguage then to create language file run::

    python manage.py makemessages -i venv --all

6. Visit the ``/accounts/`` URL to access user account.

7. To create multilanguage url you need to have ``locale/<language-code>`` directory, then run::

    python manage.py makemessages --all -i venv
    # then make your changes in your local file after run
    python manage.py compilemessages


Notes:
--------

- static/notify :: Ref: https://github.com/deviserops/notify
- static/justify :: Ref: https://github.com/deviserops/justify
- static/images