# MIPYTGitHubBot
GitHub Issues Bot for MI-PYT in FIT CTU in Prague. The program has two modes: console and web app. In *console* mode it labels issues (checks new one with the specified frequency) in the given repository by the issues itself and their comments, and in *web* mode the program labels new opened issue as soon as possible (by [webhook](https://developer.github.com/webhooks/) notification and so one by one). 

### Requirements
* python 3.5
* libraries: [click](http://click.pocoo.org/6/), [requests](http://docs.python-requests.org/en/master/), [json](http://docs.python.org/3.5/library/json.html), [configparser](http://docs.python.org/3.5/library/configparser.html), [re](http://docs.python.org/3.5/library/re.html), [sched](http://docs.python.org/3.5/library/sched.html), [time](http://docs.python.org/3.5/library/time.html), [flask](http://flask.pocoo.org/), [hashlib](https://docs.python.org/3/library/hashlib.html), [hmac](https://docs.python.org/3/library/hmac.html), [logging](https://docs.python.org/3/library/logging.html), [pandoc](http://pandoc.org/), [pypandoc](https://pypi.python.org/pypi/pypandoc), [appdirs](https://pypi.python.org/pypi/appdirs)

### Manual
First, create **auth.cfg** (with GitHub personal access token), **label.cfg** (with available labels and the appropriate rules as regular expressions), **secret.cfg** (with [webhook secret token](https://developer.github.com/webhooks/securing/)) and **web.cfg** (web app uses it for reading info about other configuration files) files with the same structure as in **./githubissuesbot/config** directory.

If you want to deploy this app on some host (tested on [pythonanywhere](https://www.pythonanywhere.com/)), don't forget to manually fix **web_config_file** value in **web_app.py** on line 41.

Link to [TODO:testpypi]()

Type --help for command line manual.
