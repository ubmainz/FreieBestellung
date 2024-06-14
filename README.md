# FreieBestellung
Webformular für die freie Bestellung von Zeitschriften (Journals) in FOLIO

## Installation

This script is based on the Python lightweight web framework [Flask](https://flask.palletsprojects.com/en/3.0.x/). To install this script Python 3.9 or later is required. Also the Python library "requests" is needed.

To install this script check out these repository files to your project folder. e.g. ~/projects

```bash
user@host:~/projects# git clone git@github.com:ubmainz/FreieBestellung.git
```

Create a virtual Python environment in your project folder ...
```bash
user@host:~/projects# cd FreieBestellung

user@host:~/projects/FreieBestellung# python -m venv .venv
```

... and activate the virtual environment:
```bash
user@host:~/projects/FreieBestellung# . .venv/bin/activate
```

Now install the libraries "Flask" and "requests" with the packet manager pip
```bash
(.venv) user@host:~/projects/FreieBestellung# pip install Flask

(.venv )user@host:~/projects/FreieBestellung# pip install requests
```

In a development setting the app can now been run with
```bash
(.venv) user@host:~/projects/FreieBestellung# flask run [--debug]
```

The Flask framework will start by default on Port 5000.

## Configuration

### Connection to FOLIO

To connect the script with a running FOLIO instance the Connection Object needs to be configured correctly.

Therefore create a script user in your FOLIO instance. Make sure that the script user is allowed to create Items in your FOLIO instance. The required permission is: 

inventory-storage.items.item.post

It may be necessary to turn on the hidden permissions in FOLIO first to set this permission for the script user.

Now you can configure your connection in connection.ini.

e.g.:

```ini
okapi_url=https://folio.your-domain.de/okapi/
url_auth_login=https://folio.your-domain.de/okapi/authn/login
tenant_id=ubxyz
username=scriptuser
password=topsecret
```

### Application

The application itself can be configured in the file

```bash
/theapp/config.py
```
