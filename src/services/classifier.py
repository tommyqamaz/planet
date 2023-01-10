from typing import List, Dict
import numpy as np
import onnxruntime as ort

from src.services.preprocess_utils import onnx_preprocessing


class Classifier:
    def __init__(self, config: Dict):
        self._onnx_path = config["model_path"]
        self._provider = config["provider"]
        self._classes = np.array(config["classes"])
        self._thresholds = np.array(config["ths"])
        self._ort_session = ort.InferenceSession(
            self._onnx_path,
            providers=[self._provider],
        )

    def get_classes(self, as_list=True):
        if as_list:
            return self._classes.tolist()
        return self._classes

    def predict_proba(self, img: np.ndarray) -> np.ndarray:

        onnx_input_tensor = onnx_preprocessing(img)
        ort_inputs = {self._ort_session.get_inputs()[0].name: onnx_input_tensor}
        ort_outputs = self._ort_session.run(None, ort_inputs)[0]

        return ort_outputs.flatten().tolist()

    def predict_classes(self, img: np.ndarray) -> List:

        predictions = self.predict_proba(img)
        result = (predictions > self._thresholds).astype(int)

        return self.get_classes(as_list=False)[result.astype(bool).flatten()].tolist()
