from httpx_oauth.clients.github import GitHubOAuth2
from httpx_oauth.clients.openid import OpenID

from app.core.settings import settings

google_oauth_client = OpenID(
    client_id=settings.GOOGLE_OAUTH_CONFIG.CLIENT_ID,
    client_secret=settings.GOOGLE_OAUTH_CONFIG.CLIENT_SECRET,
    openid_configuration_endpoint='https://accounts.google.com/.well-known/openid-configuration'
)
github_oauth_client = GitHubOAuth2(
    client_id=settings.GITHUB_OAUTH_CONFIG.CLIENT_ID,
    client_secret=settings.GITHUB_OAUTH_CONFIG.CLIENT_SECRET
)
