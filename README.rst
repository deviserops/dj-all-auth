===============
DJ All Auth
===============

``Django all auth`` includes all account, including django default, OAuth (Google, Discord, Twitch), openId (Steam).

Detailed documentation is in the "docs" directory.

Demo Images:
------------

    Login/Signup Page

    .. image:: ./docs/images/login.png
        :align: center

Quick start
-----------
1. Install it by::

    https://pypi.org/project/dj-all-auth/

    pip install dj-all-auth

2. Add "dj_all_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        'dj_all_auth',
    ]

3. Include the polls URLconf in your project urls.py like this::

    # if you are not using /accounts url then you need to add `LOGIN_URL = '<your-url>'` in your settings.py, and use that url to url path.

    path('accounts/', include('dj_all_auth.urls')),


4. Add context processor to settings.py::

    'dj_all_auth.context_processors.__config'


5. Add dj_all_auth settings to settings.py::

    DJ_ALL_AUTH = {
        # static path of logo image
        'LOGO': None,
        'CONNECTIONS': {
            # name of the url that will be used once OAuth is completed
            'REDIRECT_URI_NAME': None,
            'GOOGLE': {
                # Set {domain-with-above-url-without-locale (en/gb)}/accounts/google/authenticated to google redirect url in google developer console
                'CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID') if os.getenv('GOOGLE_CLIENT_ID') else None,
                'CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET') if os.getenv('GOOGLE_CLIENT_SECRET') else None,
                'SCOPE': ['openid', 'email', 'https://www.googleapis.com/auth/drive.file']
            },
            'TWITCH': {
                # Set {domain-with-above-url-without-locale (en/gb)}/account/twitch/authenticated to twitch redirect url in twitch developer console
                'CLIENT_ID': os.getenv('TWITCH_CLIENT_ID') if os.getenv('TWITCH_CLIENT_ID') else None,
                'CLIENT_SECRET': os.getenv('TWITCH_CLIENT_SECRET') if os.getenv('TWITCH_CLIENT_SECRET') else None,
                'SCOPE': ['openid', 'user:read:email', 'user:read:broadcast']
            },
            'DISCORD': {
                # Set {domain-with-above-url-without-locale (en/gb)}/account/discord/authenticated to discord redirect url in discord developer console
                'CLIENT_ID': os.getenv('DISCORD_CLIENT_ID') if os.getenv('DISCORD_CLIENT_ID') else None,
                'CLIENT_SECRET': os.getenv('DISCORD_CLIENT_SECRET') if os.getenv('DISCORD_CLIENT_SECRET') else None,
                'SCOPE': ['identify', 'email', 'connections', 'guilds', 'guilds.join']
            }
        }
    }

6. To create migrations run::

    python manage.py migrate

7. If you are using multilanguage then to create language file run::

    python manage.py makemessages --all -i venv

8. Visit the ``/accounts/`` URL to access user account.

9. To create multilanguage url you need to have ``locale/<language-code>`` directory, then run::

    python manage.py makemessages --all -i venv
    # then make your changes in your local file then run
    python manage.py compilemessages


Notes:
------

 These are additional packages used for UI stability - You can find them on my profile.

- static/notify :: Ref: https://github.com/deviserops/notify
- static/justify :: Ref: https://github.com/deviserops/justify
- static/images :: All static images are present in this dir, replace them as required (Must be same name and type.)

--------

 Test, Build and upload.

- `python -m build`
- `pip install --user django-all-auth/dist/path_to.tar.gz` To run on local
- `twine upload dist/* --verbose`