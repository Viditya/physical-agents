"""Common base interface for vision-spatial AI providers."""

from abc import ABC, abstractmethod


class VisionProvider(ABC):
    """Abstract base class for image-understanding providers."""

    @abstractmethod
    def describe_image(self, image_path: str, prompt: str) -> dict:
        """Analyse *image_path* using *prompt* and return a result dict.

        Returns:
            dict with at minimum a "description" key containing the model
            response and a "provider" key identifying the implementation.
        """
