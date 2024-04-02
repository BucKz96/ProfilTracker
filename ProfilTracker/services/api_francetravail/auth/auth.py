import logging
from dotenv import load_dotenv
from fastapi import HTTPException
import httpx
import os
import time


load_dotenv()


class FranceTravailAuth:

    def __init__(self) -> None:
        self.logger = logging.getLogger(os.getenv("SERVICE_NAME"))
        self.CLIENT_ID = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")
        self.URL_TOKEN = os.getenv("FRANCE_TRAVAIL_URL_TOKEN")
        self.SCOPES = os.getenv("FRANCE_TRAVAIL_SCOPES")
        self.CREDENTIALS = os.getenv("FRANCE_TRAVAIL_CREDENTIALS")
        self.access_token = None
        self.token_expires_at = 0

    async def fetch_access_token(self, force_refresh=False):

        if (
            self.access_token
            and self.token_expires_at > time.time()
            and not force_refresh
        ):
            self.logger.info("Utilisation du token existant.")
            return self.access_token

        self.logger.info("Récupération d'un nouveau token...")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {
            "grant_type": self.CREDENTIALS,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "scope": self.SCOPES,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.URL_TOKEN, headers=headers, data=data
            )

            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data["access_token"]
                self.token_expires_at = time.time() + token_data["expires_in"]
                self.logger.info("Token récupéré avec succès.")
                return self.access_token
            else:
                self.logger.error(
                    f"""Erreur lors de la récupération du token :
                    {response.status_code} - {response.text}"""
                )
                raise HTTPException(f"Erreur API: {response.status_code}")
