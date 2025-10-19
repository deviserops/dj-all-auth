===============
DJ All Auth
===============

``Django all auth`` includes all account, including django default, OAuth (Google, Discord, Twitch), openId (Steam).

Detailed documentation is in the "docs" directory.

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

    path('connection/', include('dj_all_auth.urls')),


4. Add dj_all_auth settings to settings.py::

    DJ_ALL_AUTH = {
        'CONNECTIONS': {
            # name of the url that will be used once OAuth is completed
            'REDIRECT_URI_NAME': None,
            'GOOGLE': {
                # Set {domain-with-above-url-without-locale (en/gb)}/connection/google/authenticated to google redirect url in google developer console
                'CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID') if os.getenv('GOOGLE_CLIENT_ID') else None,
                'CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET') if os.getenv('GOOGLE_CLIENT_SECRET') else None,
                'SCOPE': ['openid', 'email', 'https://www.googleapis.com/auth/drive.file']
            },
            'TWITCH': {
                # Set {domain-with-above-url-without-locale (en/gb)}/connection/twitch/authenticated to twitch redirect url in twitch developer console
                'CLIENT_ID': os.getenv('TWITCH_CLIENT_ID') if os.getenv('TWITCH_CLIENT_ID') else None,
                'CLIENT_SECRET': os.getenv('TWITCH_CLIENT_SECRET') if os.getenv('TWITCH_CLIENT_SECRET') else None,
                'SCOPE': ['openid', 'user:read:email', 'user:read:broadcast']
            },
            'DISCORD': {
                # Set {domain-with-above-url-without-locale (en/gb)}/connection/discord/authenticated to discord redirect url in discord developer console
                'CLIENT_ID': os.getenv('DISCORD_CLIENT_ID') if os.getenv('DISCORD_CLIENT_ID') else None,
                'CLIENT_SECRET': os.getenv('DISCORD_CLIENT_SECRET') if os.getenv('DISCORD_CLIENT_SECRET') else None,
                'SCOPE': ['identify', 'email', 'connections', 'guilds', 'guilds.join']
            }
        }
    }

6. To create migrations run::

    python manage.py migrate

8. Now you can simply hit the login url and All Done, you will be logged in using appropriate requested connection.::

    For ex: `connection/google/authenticate` and you will be redirect to login page for google.



Test, Build and upload.:
------------------------


- `python -m build`
- `pip install --user django-all-auth/dist/path_to.tar.gz` To run on local
- `============================`
- First Test Upload
- `python3 -m twine upload --repository testpypi dist/*`
- `============================`
- Then Live Upload
- `twine upload dist/* --verbose`