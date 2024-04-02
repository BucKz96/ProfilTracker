# conftest.py

import pytest
import asyncio
from uvicorn import Config, Server


@pytest.fixture(scope="module")
async def test_app():
    from app import app  # Importez votre application FastAPI ici

    config = Config(app=app, host="127.0.0.1", port=8000, log_level="info")
    server = Server(config=config)

    loop = asyncio.get_event_loop()
    serve_task = loop.create_task(server.serve())
    await asyncio.sleep(3)  # Attendre que le serveur soit opérationnel

    yield  # Ici, vos tests s'exécuteront

    serve_task.cancel()  # Arrêtez le serveur une fois les tests terminés
    await asyncio.sleep(
        1
    )  # Laissez le temps au serveur de s'arrêter proprement
