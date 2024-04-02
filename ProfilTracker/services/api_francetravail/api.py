import os
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()


class FranceTravailAPI:
    def __init__(self, auth):
        self.SERVICE_INFO = os.getenv("SERVICE_INFO")
        self.FRANCE_TRAVAIL_URL_TEST = os.getenv("FRANCE_TRAVAIL_URL_TEST")
        self.auth = auth
        self.logger = auth.logger

    async def get_status(self):
        self.logger.info("Fetching status from France Travail API")
        status_details = {
            "status": "checking",
            "details": {
                "franceTravailApi": "unknown",
                "tokenValidity": "unknown",
            },
        }
        headers = {"Authorization": f"Bearer {self.auth.access_token}"}
        test_url = self.FRANCE_TRAVAIL_URL_TEST
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(test_url, headers=headers)
                if response.status_code == 200:
                    status_details["details"]["franceTravailApi"] = "available"
                    status_details["details"]["tokenValidity"] = "valid"
                    status_details["status"] = "up"
                    self.logger.info(
                        """API France Travail is operational and the access
                          token is valid."""
                    )
                else:
                    status_details["status"] = "down"
                    status_details["details"][
                        "franceTravailApi"
                    ] = "issue detected"
                    self.logger.error(
                        f"Failed to verify API status: {response.status_code} \
                        - {response.text}"
                    )
            except httpx.RequestError as e:
                status_details["status"] = "down"
                status_details["details"]["franceTravailApi"] = "unreachable"
                self.logger.error(
                    f"Error connecting to the API France Travail: {e}"
                )
        return status_details

    async def get_data(self):
        data_endpoint = os.getenv("DATA_ENDPOINT")
        base_url = os.getenv("EXTERNAL_API_BASE_URL")
        url = f"{base_url}/{data_endpoint}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                self.logger.info(f"Successful data fetch from {url}")
                return response.json()
            except httpx.HTTPStatusError as e:
                self.logger.error(
                    f"API call error: {e.response.status_code} for {url}. \
                    Response: {e.response.text}"
                )
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail="Error during the external API call.",
                )
            except httpx.RequestError as e:
                self.logger.error(
                    f"Network error during API call for {url}: {e}"
                )
                raise HTTPException(
                    status_code=500,
                    detail="""Network error during the call to
                    the external API.""",
                )

    def get_info(self):
        self.logger.info("Fetching service info")
        return self.SERVICE_INFO
