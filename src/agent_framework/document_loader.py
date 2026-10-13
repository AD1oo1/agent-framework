from pathlib import Path
from typing import Protocol

from agent_framework.document import Document


class DocumentLoader(Protocol):

    def load(self, path: str | Path) -> list[Document]:
        ...
