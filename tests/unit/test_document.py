from agent_framework.document import Document


def test_document_stores_content_and_metadata():

    document = Document(
        content="Revenue increased by 10%.",
        metadata={
            "source": "annual_report.pdf",
            "page": 12,
        },
    )

    assert document.content == (
        "Revenue increased by 10%."
    )

    assert document.metadata["source"] == (
        "annual_report.pdf"
    )

    assert document.metadata["page"] == 12


def test_document_defaults_metadata_to_empty_dict():

    document = Document(
        content="Sample document."
    )

    assert document.metadata == {}
