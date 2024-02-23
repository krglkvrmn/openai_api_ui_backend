from dataclasses import dataclass

from fastapi import Response, status
from fastapi_users import models
from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication.strategy import StrategyDestroyNotSupportedError
from fastapi_users.authentication.transport import TransportLogoutNotSupportedError
from fastapi_users.types import DependencyCallable


@dataclass
class TokenPair:
    access_token: str
    refresh_token: str

    def __repr__(self):
        return f'access_token={self.access_token[:10]}..., refresh_token={self.refresh_token[:10]}'


class JWTWithRefreshStrategyWriteOnly:
    """
    Strategy for issuing a pair of JWT tokens on login.
    Requires setting two sub-strategies for access and refresh tokens.
    WARNING: This strategy works only for issuing tokens and unable to check their validity
    """
    def __init__(self, access_token_strategy, refresh_token_strategy):
        self.access_token_strategy = access_token_strategy
        self.refresh_token_strategy = refresh_token_strategy

    async def write_tokens(self, user: models.UP) -> TokenPair:
        return TokenPair(
            access_token=await self.access_token_strategy.write_token(user),
            refresh_token=await self.refresh_token_strategy.write_token(user)
        )

    async def destroy_tokens(self, tokens: TokenPair, user: models.UP) -> None:
        raise StrategyDestroyNotSupportedError("A JWT can't be invalidated: it's valid until it expires.")


class AccessRefreshTokensCookieTransport(CookieTransport):
    def __init__(
            self,
            access_token_cookie_transport: CookieTransport,
            refresh_token_cookie_transport: CookieTransport
    ):
        self.access_token_cookie_transport = access_token_cookie_transport
        self.refresh_token_cookie_transport = refresh_token_cookie_transport

    async def get_login_response(self, tokens: TokenPair) -> Response:
        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        response = self.access_token_cookie_transport._set_login_cookie(response, tokens.access_token)
        return self.refresh_token_cookie_transport._set_login_cookie(response, tokens.refresh_token)

    async def get_logout_response(self) -> Response:
        response = Response(status_code=status.HTTP_204_NO_CONTENT)
        response = self.access_token_cookie_transport._set_logout_cookie(response)
        return self.refresh_token_cookie_transport._set_logout_cookie(response)


class AccessRefreshAuthenticationBackend:
    name: str
    transport: AccessRefreshTokensCookieTransport

    def __init__(
            self,
            name: str,
            transport: AccessRefreshTokensCookieTransport,
            get_strategy: DependencyCallable[JWTWithRefreshStrategyWriteOnly],
    ):
        self.name = name
        self.transport = transport
        self.get_strategy = get_strategy

    async def login(self, strategy: JWTWithRefreshStrategyWriteOnly, user: models.UP) -> Response:
        tokens = await strategy.write_tokens(user)
        return await self.transport.get_login_response(tokens)

    async def logout(self, strategy: JWTWithRefreshStrategyWriteOnly, user: models.UP, token: str) -> Response:
        try:
            await strategy.destroy_tokens(token, user)
        except StrategyDestroyNotSupportedError:
            pass

        try:
            response = await self.transport.get_logout_response()
        except TransportLogoutNotSupportedError:
            response = Response(status_code=status.HTTP_204_NO_CONTENT)

        return response

