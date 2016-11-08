from flask import Flask
from flask import render_template
from flask import request
import configparser
import hashlib
import hmac
import markdown
import appdirs
from socket import gethostname
import pkg_resources


def _read_web_config():
    """
    This function reads *web_config_file* and storing paths to other
    configuration files (auth.cfg, label.cfg and secret.cfg) and reading
    secret token value from the appropriate file.
    """
    global conf
    conf.read(web_config_file)

    global secret_file
    secret_file = conf['github']['secret_file']

    global auth_file
    auth_file = conf['github']['auth_file']

    global label_file
    label_file = conf['github']['label_file']

    # read file with a secret token for webhook
    conf.read(secret_file)


app_name = __name__.split('.')[0]
app = Flask(app_name)
conf = configparser.ConfigParser()

# if it is running on pythonanywhere.com (maybe that code works for other hosts)
if 'liveweb' in gethostname():
    import github_bot
    # set "web_config_file" variable to file with web configuration
    # format: /home/<username>/<project_name>/path/to/webcfg.cfg
    web_config_file = '/home/bobirdmi/MIPYTBotTMP/githubissuesbot/config/web.cfg'
    # read web configurations
    _read_web_config()
else:
    from . import github_bot


@app.route('/')
def index():
    """
    This function generates HTML formatted main page from README.md.
    """
    readme_text = pkg_resources.resource_stream(app_name, 'README.md')

    return render_template('index.html', readme_text=readme_text.read().decode("utf-8"))


@app.route('/hook', methods=['POST'])
def hook():
    """
    The function handles labeling GitHub issues by receiving GitHub webhook POST requests.
    See https://developer.github.com/webhooks/

    First, webhook signature (in header "X-Hub-Signature") is verified for security reasons
    as we don't want to handle undesirable requests. Then :py:func:`github_bot.GitHubBot`  class is used for
    issue labeling.
    """
    verify_signature(conf['github']['secret_token'],
                     request.headers['X-Hub-Signature'],
                     request.data)

    req_json = request.get_json()
    if req_json['action'] == 'opened':
        bot = github_bot.GitHubBot(auth_file, label_file, None, 'default')
        bot.label_issue(req_json['issue'])

    return str(req_json['issue']['url']) + ', ' + str(req_json['issue']['title']) + ', ' \
           + str(req_json['issue']['body']) + ', ' + str(req_json['issue']['labels']) + ', ' \
           + str(req_json['action'])


@app.template_filter('markdown')
def convert_markdown(text):
    """
    Custom Flask template filter. Converts markdown text to safe html.

    Args:
        text (str): Markdown formatted text as Unicode or ASCII string.
    """
    return markdown.markdown(text)


def verify_signature(secret: str, signature: str, resp_body) -> None:
    """
    Verify HMAC-SHA1 signature of the given response body.
    The signature is expected to be in format ``sha1=<hex-digest>``.

    Args:
        secret (str): GitHub webhook secret token. See https://developer.github.com/webhooks/securing/
        signature (str): SHA1 signature from webhook request (from header "X-Hub-Signature").
        resp_body (str): Webhook request body.

    Raises:
        Exception: Error: signature is malformed.
        Exception: Error: expected type sha1.
        Exception: Error: digests do not match.

    .. testsetup::

       from githubissuesbot import web_app

       fake_secret = '3ce92e588556bdh7220bc738b4dafad15bj7c196'
       body = 'this is my signature!'.encode('utf-8')
       good_signature = 'sha1=18fdf73c44d3a4b72b55b382c494f35a25b3a6e5'

    .. testcode::
       :hide:

       web_app.verify_signature(fake_secret, good_signature, body)

    Verification of bad signature

    .. testcode::

       bad_signature = 'sha1=18fdf73c44d3a4c72b55b382c494f35a25b3a6e5'
       web_app.verify_signature(fake_secret, bad_signature, body)

    .. testoutput::

       Traceback (most recent call last):
           ...
       Exception: Error: digests do not match

    The following signature is broken: there is no '=' between hash type and signature itself

    .. testcode::

       bad_signature2 = 'sha118fdf73c44d3a4c72b55b382c494f35a25b3a6e5'
       web_app.verify_signature(fake_secret, bad_signature2, body)

    .. testoutput::

       Traceback (most recent call last):
           ...
       Exception: Error: signature is malformed

    The last signature is hashed by unsupported hash type (sha2)

    .. testcode::

       bad_signature3 = 'sha2=18fdf73c44d3a4c72b55b382c494f35a25b3a6e5'
       web_app.verify_signature(fake_secret, bad_signature3, body)

    .. testoutput::

       Traceback (most recent call last):
           ...
       Exception: Error: expected type sha1, but got sha2

    """
    try:
        alg, digest = signature.lower().split('=', 1)
    except (ValueError, AttributeError):
        raise Exception('Error: signature is malformed')

    if alg != 'sha1':
        raise Exception("Error: expected type sha1, but got %s" % alg)

    computed_digest = hmac.new(secret.encode('utf-8'),
                               msg=resp_body,
                               digestmod=hashlib.sha1).hexdigest()

    if not hmac.compare_digest(computed_digest, digest):
        raise Exception('Error: digests do not match')


def run_local_web(web_config):
    """
    Runs local Flask server.

    Args:
        web_config (str): File with main web configuration. If None, the default file *web.cfg* will be used.
    """
    global web_config_file
    if web_config:
        web_config_file = web_config
    else:
        web_config_file = appdirs.site_config_dir(appname=app_name) + '/web.cfg'

    # read web configuration
    _read_web_config()

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
