from pathlib import Path

from pypdf import PdfReader

from agent_framework.document import Document


class PDFLoader:

    def load(
        self,
        path: str | Path,
    ) -> list[Document]:

        file_path = Path(path)

        reader = PdfReader(file_path)

        documents = []

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            content = page.extract_text() or ""

            documents.append(
                Document(
                    content=content,
                    metadata={
                        "source": str(file_path),
                        "type": "pdf",
                        "page": page_number,
                    },
                )
            )

        return documents
