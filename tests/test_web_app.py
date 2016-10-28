import pytest
import markdown
from githubissuesbot.web_app import app


@pytest.fixture
def testapp():
    app.config['TESTING'] = True
    return app.test_client()


def test_main_page(testapp):
    with open('README.md', 'r') as f:
        assert markdown.markdown(f.read()) in testapp.get('/').data.decode('utf-8')


