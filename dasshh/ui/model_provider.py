from typing import Callable
from functools import partial
from textual.command import Provider, Hits, DiscoveryHit, Hit


class ModelProvider(Provider):
    """A Provider for models."""

    @property
    def commands(self) -> list[tuple[str, Callable[[], None]]]:
        models = self.app.available_models

        def set_model(model: str) -> None:
            self.app.selected_model = model

        return [
            (model, partial(set_model, model))
            for model in models
        ]

    async def discover(self) -> Hits:
        """Discover models."""
        for command in self.commands:
            yield DiscoveryHit(*command)

    async def search(self, query: str) -> Hits:
        """Search for models."""
        matcher = self.matcher(query)

        for name, callback in self.commands:
            if (match := matcher.match(name)) > 0:
                yield Hit(match, matcher.highlight(name), callback)
