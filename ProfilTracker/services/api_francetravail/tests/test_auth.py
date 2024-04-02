import pytest
from services.api_francetravail.auth.auth import FranceTravailAuth


@pytest.mark.asyncio
async def test_fetch_access_token():
    authenticator = FranceTravailAuth()
    token = await authenticator.fetch_access_token()

    assert token is not None
    assert isinstance(token, str)
    assert authenticator != 0
