# A simple bookmark app

## Features
* User authentication using emails, profiles, custom user( account app)
* Social authentication via Twitter, Facebook, Google( account app)
* Able to bookmark images from different sites( images app)
* share images what you bookmark( images app)
* shows number of likes and ability to like an image bookmarked by others( actions app)
* updated count of views and ranking by number of likes and views( actions app and account)
* follow people who are register on the account( account )
* local SSH

## Tools:
* Python and Django
* Bootstrap as CSS and Js
* django signal demoralization in this case I use m2m_changed signal
* Redis to handle the user likes count and user views count
* Django debug toolbar which is very helpful debugging tool
* poetry for dependency management

## Todo
* Add Testing
* Add search functionality
* Add messaging
* improve UI

# How to run a local Django development server over HTTPS with a trusted self-signed SSL certificate

## Tools used
- https://github.com/FiloSottile/mkcert

## MacOs
`brew install mkcert`

* Then, make your Operational system trust the local certificates we're about to generate by install the certificate authority(CA)
`mkcert -install`

* Next you need to generate a certificate for the localhost domain. So, go to your root Django project and run the following command
`mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1`
Note: you can also add another host if you use other than localhost

## Configuring Django server to work with HTTPS
1. Run the following command to install Django extensions alongwith the Wekzeug server:

`pip install django-extensions Werkzeug`

The *runserver_plus* command requires installation of the Werkzeug server.

2. Next, open the settings.py file in your code editor and add django_extensions to the INSTALLED_APPS list:

```
INSTALLED_APPS = [
    # other apps
    "django_extensions",
]
```
Finally, start the local development server in HTTPS mode by running the command:

`python manage.py runserver_plus --cert-file cert.pem --key-file key.pem`

And that's it; you should now see the local development server running at the default https://localhost:8000 address.


# Create a profile for users that register with social authentication
 `Python Social Auth uses a pipeline consisting of a set of functions that are executed in a specific order executed during the authentication flow. These functions take care of retrieving any user details, creating a social profile in the database, and asso- ciating it to an existing user or creating a new one.`

 So, we are going to add a new step to the pipeline to automatically create a profile object in the database when a new user is created.

- Add the following `SOCIAL_AUTH_PIPELINE` to the `settings.py`

```
SOCIAL_AUTH_PIPELINE = [
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
]
```

`Desclaimer: This is based on the Django 4 by example `