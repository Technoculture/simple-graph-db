"""
Provide access to different embeddings models
"""

from abc import ABC, abstractmethod
import openai


class EmbeddingsModel(ABC):
    @abstractmethod
    def get_embedding(self, text: str) -> list[float]:
        pass


class OpenAIEmbeddingsModel(EmbeddingsModel):
    def __init__(
        self, embed_client: openai.OpenAI, embed_model: str, embed_dimension: int
    ) -> None:
        self.client = embed_client if embed_client else None
        self.model = embed_model
        self.dimension = embed_dimension

    def get_embedding(self, text: str) -> list[float]:
        if self.client is None:
            return []
        text = text.replace("\n", " ")
        return (
            self.client.embeddings.create(
                input=[text],
                model=self.model,
                dimensions=self.dimension,
                encoding_format="float",
            )
            .data[0]
            .embedding
        )
