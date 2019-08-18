import pytest
from reporting_app.app import create_app
from reporting_app.settings import TestConfig

@pytest.yield_fixture(scope='function')
def app():
    return create_app(TestConfig)