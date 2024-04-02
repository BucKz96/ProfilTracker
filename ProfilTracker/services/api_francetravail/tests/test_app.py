import httpx
import pytest


@pytest.mark.asyncio
async def test_get_status():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "up"
