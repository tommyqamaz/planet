from dependency_injector import containers, providers

from src.services.classifier import Classifier


class AppContainer(containers.DeclarativeContainer):
    """Create di container."""

    config = providers.Configuration()

    classifier = providers.Singleton(
        Classifier,
        config=config.services.classifier,
    )
