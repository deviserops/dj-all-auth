===============
Django All Auth
===============

Django all auth includes all account, including django default, OAuth (Google, Discord, Twitch), openId (Steam).

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "account" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        'django_all_auth',
    ]

2. Include the polls URLconf in your project urls.py like this::

    # if you are not using /accounts url then you need to add `LOGIN_URL = '<your-url>'` in your settings.py

    path('accounts/', include('django_all_auth.urls')),


3. Add context processor to settings.py::

    'django_all_auth.context_processors.__config'


4. To create models run::

    python manage.py migrate

5. If you are using multilangual then to create language file run::

    python manage.py makemessages -i venv --all

6. Visit the ``/accounts/`` URL to access user account.
