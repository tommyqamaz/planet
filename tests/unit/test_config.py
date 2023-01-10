import pytest

from omegaconf import OmegaConf


def test_conf():
    conf = OmegaConf.load("configs/config.yml")
    assert isinstance(conf.services.classifier.model_path, str)
    assert isinstance(conf.services.classifier.provider, str)
    assert isinstance(conf.services.classifier.ths[0], float)
    assert isinstance(conf.services.classifier.classes[0], str)
