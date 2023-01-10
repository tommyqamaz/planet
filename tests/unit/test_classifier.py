from copy import deepcopy

import numpy as np

from src.containers.containers import AppContainer


def test_predicts_not_fail(app_container: AppContainer, sample_image_np: np.ndarray):
    classifier = app_container.classifier()
    classifier.predict_classes(sample_image_np)
    classifier.predict_proba(sample_image_np)
    classifier.get_classes()


def test_predicts_are_list(app_container: AppContainer, sample_image_np: np.ndarray):
    classifier = app_container.classifier()
    result = classifier.predict_classes(sample_image_np)
    assert isinstance(result, list)
    assert len(result) > 0


def test_prob_less_or_equal_to_one(
    app_container: AppContainer, sample_image_np: np.ndarray
):

    poster_classifier = app_container.classifier()
    probs = poster_classifier.predict_proba(sample_image_np)
    for prob in probs:
        assert prob < 1
        assert prob > 0


def test_predict_dont_mutate_initial_image(
    app_container: AppContainer, sample_image_np: np.ndarray
):

    initial_image = deepcopy(sample_image_np)
    classifier = app_container.classifier()
    classifier.predict_classes(sample_image_np)

    assert np.allclose(initial_image, sample_image_np)
