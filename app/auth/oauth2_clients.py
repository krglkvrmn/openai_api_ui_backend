from httpx_oauth.clients.github import GitHubOAuth2
from httpx_oauth.clients.openid import OpenID

from app.core.config import (
    GITHUB_OAUTH2_CLIENT_ID, GITHUB_OAUTH2_CLIENT_SECRET, GOOGLE_OAUTH2_CLIENT_ID,
    GOOGLE_OAUTH2_CLIENT_SECRET
)

google_oauth_client = OpenID(
    client_id=GOOGLE_OAUTH2_CLIENT_ID,
    client_secret=GOOGLE_OAUTH2_CLIENT_SECRET,
    openid_configuration_endpoint='https://accounts.google.com/.well-known/openid-configuration'
)
github_oauth_client = GitHubOAuth2(
    client_id=GITHUB_OAUTH2_CLIENT_ID,
    client_secret=GITHUB_OAUTH2_CLIENT_SECRET
)
