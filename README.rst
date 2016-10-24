MIPYTGitHubBot
==============

GitHub Issues Bot for MI-PYT in FIT CTU in Prague. The program has two
modes: console and web app. In *console* mode it labels issues (checks
new one with the specified frequency) in the given repository by the
issues itself and their comments, and in *web* mode the program labels
new opened issue as soon as possible (by
`webhook <https://developer.github.com/webhooks/>`__ notification and so
one by one).

Requirements
~~~~~~~~~~~~

-  python 3.5
-  libraries: `click <http://click.pocoo.org/6/>`__,
   `requests <http://docs.python-requests.org/en/master/>`__,
   `json <http://docs.python.org/3.5/library/json.html>`__,
   `configparser <http://docs.python.org/3.5/library/configparser.html>`__,
   `re <http://docs.python.org/3.5/library/re.html>`__,
   `sched <http://docs.python.org/3.5/library/sched.html>`__,
   `time <http://docs.python.org/3.5/library/time.html>`__,
   `flask <http://flask.pocoo.org/>`__,
   `hashlib <https://docs.python.org/3/library/hashlib.html>`__,
   `hmac <https://docs.python.org/3/library/hmac.html>`__,
   `logging <https://docs.python.org/3/library/logging.html>`__,
   `pandoc <http://pandoc.org/>`__,
   `pypandoc <https://pypi.python.org/pypi/pypandoc>`__,
   `appdirs <https://pypi.python.org/pypi/appdirs>`__

Manual
~~~~~~

First, create **auth.cfg** (with GitHub personal access token),
**label.cfg** (with available labels and the appropriate rules as
regular expressions), **secret.cfg** (with `webhook secret
token <https://developer.github.com/webhooks/securing/>`__) and
**web.cfg** (web app uses it for reading info about other configuration
files) files with the same structure as in **./githubissuesbot/config**
directory.

If you want to deploy this app on some host (tested on
`pythonanywhere <https://www.pythonanywhere.com/>`__), don't forget to
manually fix **web\_config\_file** value in **web\_app.py** on line 41.

Link to `testpypi <https://testpypi.python.org/pypi/githubissuesbot>`__

Type --help for command line manual.
