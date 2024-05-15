import instructor
from abc import ABC, abstractmethod

from personal_graph.clients import LLMClient
from personal_graph.models import KnowledgeGraph


class GraphGenerator(ABC):
    @abstractmethod
    def generate(self, query: str) -> KnowledgeGraph:
        """Generate a KnowledgeGraph from the given query."""
        pass


class InstructorGraphGenerator(GraphGenerator):
    def __init__(
        self,
        llm_client: LLMClient,
        function_calling_model: str = "gpt-3.5-turbo",
        system_prompt: str = "You are a high quality knowledge graph generator based on the user query for the purpose of generating descriptive, informative, detailed and accurate knowledge graphs. You can generate proper nodes and edges as a knowledge graph.",
        prompt: str = "Help me describe this user query as a detailed knowledge graph with meaningful relationships that should provide some descriptive attributes(attribute is the detailed and proper information about the edge) and informative labels about the nodes and relationship. Try to make most of the relationships between similar nodes.",
    ):
        self.function_calling_model = function_calling_model
        self.system_prompt = system_prompt
        self.prompt = prompt
        self.llm_client = llm_client

    def generate(self, query: str) -> KnowledgeGraph:
        client = instructor.from_openai(self.llm_client.client)
        knowledge_graph = client.chat.completions.create(
            model=self.function_calling_model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": f"{self.prompt}: {query}",
                },
            ],
            response_model=KnowledgeGraph,
        )
        return knowledge_graph
