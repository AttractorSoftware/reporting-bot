import pytest, os, sys
os.environ['ENV'] = 'TEST'


@pytest.fixture
def app():
    from reporting_app.app import app
    return app
