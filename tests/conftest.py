import os.path

import cv2
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from omegaconf import OmegaConf

from app import set_routers
from src.containers.containers import AppContainer
from src.routes import planet

TESTS_DIR = os.path.dirname(__file__)
IMG_PATH = "tests/fixtures/test_2.jpg"


@pytest.fixture(scope="session")
def sample_image_bytes():
    f = open(IMG_PATH, "rb")  # noqa: WPS515
    try:
        yield f.read()
    finally:
        f.close()


@pytest.fixture
def sample_image_np():
    img = cv2.imread(IMG_PATH)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


@pytest.fixture(scope="session")
def app_config():
    return OmegaConf.load(os.path.join(TESTS_DIR, "../configs/test_config.yml"))


@pytest.fixture
def app_container(app_config):
    container = AppContainer()
    container.config.from_dict(app_config)
    return container


@pytest.fixture
def wired_app_container(app_config):
    container = AppContainer()
    container.config.from_dict(app_config)
    container.wire([planet])
    yield container
    container.unwire()


@pytest.fixture
def test_app(app_config, wired_app_container):
    app = FastAPI()
    set_routers(app)
    return app


@pytest.fixture
def client(test_app):
    return TestClient(test_app)
