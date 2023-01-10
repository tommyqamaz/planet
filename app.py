import uvicorn
from fastapi import FastAPI
from omegaconf import OmegaConf

from src.containers.containers import AppContainer
from src.routes import planet
from src.routes.routers import router as app_router

from src.consts import PORT


def set_routers(app: FastAPI):
    """Set routers.

    Args:
        app: FastAPI - fastapi application.
    """
    app.include_router(app_router, prefix="/planet", tags=["planet"])


def create_app() -> FastAPI:
    """Create FaskAPI app.

    Returns:
        FastAPI: FastAPI - fastapi application.
    """
    cfg = OmegaConf.load("configs/config.yml")
    container = AppContainer()
    container.config.from_dict(cfg)
    container.wire([planet])
    app = FastAPI()
    set_routers(app)
    return app


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, port=PORT, host="0.0.0.0")
