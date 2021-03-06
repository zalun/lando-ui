# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import binascii
import json

import pytest

from landoui.app import create_app


@pytest.fixture
def docker_env_vars(monkeypatch):
    """Monkeypatch environment variables that we'd get running under docker."""
    monkeypatch.setenv('OIDC_DOMAIN', 'test_oidc_domain')
    monkeypatch.setenv('OIDC_CLIENT_ID', 'test_oidc_client_id')
    monkeypatch.setenv('OIDC_CLIENT_SECRET', 'test_oidc_secret')


@pytest.fixture
def api_url():
    """A string holding the Lando API base URL. Useful for request mocking."""
    return 'http://lando-api.test'


@pytest.fixture
def app(versionfile, docker_env_vars, api_url):
    app = create_app(
        version_path=versionfile.strpath,
        secret_key=str(binascii.b2a_hex(os.urandom(15))),
        session_cookie_name='lando-ui',
        session_cookie_domain='lando-ui.test:7777',
        session_cookie_secure=False,
        use_https=0,
        enable_asset_pipeline=False,
        lando_api_url=api_url,
        debug=True
    )

    # Turn on the TESTING setting so that exceptions within the app bubble up
    # to the test runner.  Otherwise Flask will hide the exception behind a
    # generic HTTP 500 response, and that makes writing and debugging tests
    # much harder.
    app.config['TESTING'] = True

    return app


@pytest.fixture
def versionfile(tmpdir):
    """Provide a temporary version.json on disk."""
    v = tmpdir.mkdir('app').join('version.json')
    v.write(
        json.dumps(
            {
                'source': 'https://github.com/mozilla-conduit/lando-api',
                'version': '0.0.0',
                'commit': '',
                'build': 'test',
            }
        )
    )
    return v
