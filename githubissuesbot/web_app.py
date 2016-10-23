from flask import Flask
from flask import render_template
from flask import request
import configparser
import hashlib
import hmac
from . import github_bot
import markdown
import appdirs

app_name = __name__.split('.')[0]
print(app_name)
app = Flask(app_name)

web_config_file = appdirs.site_config_dir(appname=app_name) + '/web.cfg'
print(web_config_file)

# read web configurations
conf = configparser.ConfigParser()
conf.read(web_config_file)
# secret_file = conf['github']['secret_file']
# auth_file = conf['github']['auth_file']
# label_file = conf['github']['label_file']
# readme_file = conf['github']['readme_file']
#
# conf.read(secret_file)


@app.route('/')
def index():
    with open(readme_file, 'r') as file:
        readme_text = file.read()

    return render_template('index.html', readme_text=readme_text)


@app.route('/hook', methods=['POST'])
def hook():
    verify_signature(conf['github']['secret_token'],
                     request.headers['X-Hub-Signature'],
                     request.data)

    if request.get_json()['action'] == 'opened':
        bot = github_bot.GitHubBot(auth_file, label_file, None, 'default')
        bot.label_issue(request.get_json()['issue'])

    return str(request.get_json()['issue']['url']) + ', ' +  str(request.get_json()['issue']['title']) + ', ' \
           + str(request.get_json()['issue']['body']) + ', ' + str(request.get_json()['issue']['labels']) + ', ' \
           + str(request.get_json()['action'])


@app.template_filter('markdown')
def convert_markdown(text):
    """Convert markdown text to html"""
    return markdown.markdown(text)


def verify_signature(secret: str, signature: str, resp_body) -> None:
    """Verify HMAC-SHA1 signature of the given response body.
    The signature is expected to be in format ``sha1=<hex-digest>``.
    """
    try:
        alg, digest = signature.lower().split('=', 1)
    except (ValueError, AttributeError):
        raise 'Error: signature is malformed'

    if alg != 'sha1':
        raise("Error: expected type sha1, but got %s" % alg)

    computed_digest = hmac.new(secret.encode('utf-8'),
                               msg=resp_body,
                               digestmod=hashlib.sha1).hexdigest()

    if not hmac.compare_digest(computed_digest, digest):
        raise 'Error: digests do not match'


def run_local_web(web_config):
    global web_config_file

    if web_config:
        web_config_file = web_config

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
