# FreieBestellung
Webformular für die freie Bestellung von Zeitschriften (Journals) in FOLIO

## Running with Docker

To run the script with Docker check out the repository to your project folder. e.g. ~/projects

```bash
user@host:~/projects# git clone https://github.com/ubmainz/FreieBestellung.git
```
```bash
user@host:~/projects# cd FreieBestellung
```

Copy "config.py.tmpl" to "config.py" to configure the script.
```bash
cp config.py.tmpl config.py
```
```bash
vim config.py
```

Copy "connection.ini.tmpl" to "connection.ini" to configure the connection to your FOLIO instance.
```bash
cp connection.ini.tmpl connection.ini
```
```bash
vim connection.ini
```

Run 'docker build' to create the image.
```bash
docker build -t request-form .
```

Run 'docker run' to start the container.
```bash
docker run -d -it --name request-form -h request-form -p 8080:8080 -v request-form:/var/log/request-form request-form
```

## Configuration

### Connection to FOLIO

To connect the script with a running FOLIO instance the Connection object needs to be configured correctly.

Therefore create a script user in your FOLIO instance. Make sure that the script user is allowed to create Items in your FOLIO instance. The required permission is: 

inventory-storage.items.item.post

It may be necessary to turn on the hidden permissions in FOLIO first to set this permission for the script user.

Now you can configure your connection in connection.ini. e.g.:

```ini
okapi_url=https://folio.your-domain.de/okapi/
url_auth_login=https://folio.your-domain.de/okapi/authn/login
tenant_id=ubxyz
username=scriptuser
password=topsecret123
```

### Application

The application itself can be configured in the file:

```bash
/theapp/config.py
```

Therefore copy config.py.tmpl to config.py and adjust your personal configuration:

ENDPOINT defines the URL path to the script. e.g. https://scripts.domain.de/request .

```bash
ENDPOINT = "request"
```

CONNECTION_INI defines the file where your connection to FOLIO is configured. Normally "connection.ini".

```bash
CONNECTION_INI = "connection.ini"
```

With EXTERNAL_SYSTEM_ID_REGEX and EXTERNAL_SYSTEM_ID_ENV the users login identifier can be configured.

EXTERNAL_SYSTEM_ID_REGEX defines the format of your users identifier e.g. stored in an IDM. In FOLIO this ID needs to be stored in the users externalSystemId field (Personen App: "Externe System-ID"). 

EXTERNAL_SYSTEM_ID_ENV defines the server environment variable that is used to send the users identifier to the script. If you use a Single-Sign-On system like e.g. Shibboleth, this name can normally be configured in Shibboleth.

```bash
# Definition der externalSystemId (z.B.: Barcode => 12 Digits)
EXTERNAL_SYSTEM_ID_REGEX = "^\d{12}$"
# Server Umgebungsvariable mit der externalSystemId (z.B.: Feld in Shibboleth)
EXTERNAL_SYSTEM_ID_ENV = "HTTP_BARCODE"
```

SESSION_LOG, DEBUG_LOG and ERROR_LOG define the logfile names for this script. SESSION_LOG will be needed to cleanup hanging items with "remove_hanging_items.sh". ERROR_LOG logs all Exceptions raised by the script. DEBUG_LOG is used only, if the [Flask](https://flask.palletsprojects.com/en/3.0.x/) web server is running in DEBUG mode. It logs the whole HTTP conversation with FOLIO (all HTTP Requests with URL, Response and Bodies) and is becoming very big very fastly.

```bash
LOGFILE_PATH = "/path/to/logfiles/"

SESSION_LOG = LOGFILE_PATH + "session.app.log"
DEBUG_LOG   = LOGFILE_PATH + "debug.app.log"
ERROR_LOG   = LOGFILE_PATH + "error.app.log"
```

The HDS2 variables are used in the HTML templates to send the user back to the right HDS2 instance he is coming from...

```bash
HDS2_DOMAIN = "https://domain.hebis.de/"

HDS2_HOME_URL    = HDS2_DOMAIN + "main/ubxyz/"
HDS2_ACCOUNT_URL = HDS2_HOME_URL + "MyResearch/Home"
HDS2_HOLDS_URL   = HDS2_HOME_URL + "MyResearch/Holds"
```

## Installation in virtual Python environment

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

For use in production install the wsgi server "gunicorn" too.
```bash
(.venv) user@host:~/projects/FreieBestellung# pip install gunicorn
```

In a development setting the app can now been run with
```bash
(.venv) user@host:~/projects/FreieBestellung# flask run [--debug]
```

The Flask web server will start by default on Port 5000 and can be stopped with 'Ctrl+C'. For more information about Flask see the [Flask](https://flask.palletsprojects.com/en/3.0.x/) documentation. Afterwards the virtual environment can be stopped with "deactivate".

```bash
(.venv) user@host:~/projects/FreieBestellung# deactivate

user@host:~/projects/FreieBestellung#
```

## Cleanup hanging Items

