from pathlib import Path

from pypdf import PdfWriter

from agent_framework.pdf_loader import PDFLoader


def test_pdf_loader_loads_pages(tmp_path: Path):

    file_path = tmp_path / "sample.pdf"

    writer = PdfWriter()

    writer.add_blank_page(
        width=612,
        height=792,
    )

    writer.add_blank_page(
        width=612,
        height=792,
    )

    with file_path.open("wb") as file:
        writer.write(file)

    loader = PDFLoader()

    documents = loader.load(file_path)

    assert len(documents) == 2

    assert documents[0].metadata["source"] == (
        str(file_path)
    )

    assert documents[0].metadata["type"] == "pdf"

    assert documents[0].metadata["page"] == 1

    assert documents[1].metadata["page"] == 2
