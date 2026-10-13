from pathlib import Path

from agent_framework.document import Document


class TextLoader:

    def load(
        self,
        path: str | Path,
    ) -> list[Document]:

        file_path = Path(path)

        content = file_path.read_text(
            encoding="utf-8"
        )

        return [
            Document(
                content=content,
                metadata={
                    "source": str(file_path),
                    "type": "text",
                },
            )
        ]
