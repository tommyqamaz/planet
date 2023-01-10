import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, File

from src.containers.containers import AppContainer
from src.routes.routers import router
from src.services.classifier import Classifier


@router.get("/classes")
@inject
def classes_list(
    service: Classifier = Depends(Provide[AppContainer.classifier]),
):
    result = service.get_classes()
    return {
        "classes": result,
    }


@router.post("/predict")
@inject
def predict(
    image: bytes = File(),
    service: Classifier = Depends(Provide[AppContainer.classifier]),
):

    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    result = service.predict_classes(img)

    return {"result": result}


@router.post("/predict_proba")
@inject
def predict_proba(
    image: bytes = File(),
    service: Classifier = Depends(Provide[AppContainer.classifier]),
):

    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    return {"result": service.predict_proba(img)}
