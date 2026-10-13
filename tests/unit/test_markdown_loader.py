from pathlib import Path

from agent_framework.markdown_loader import MarkdownLoader


def test_markdown_loader_loads_file(tmp_path: Path):

    file_path = tmp_path / "sample.md"

    file_path.write_text(
        "# Financial Report\n\nRevenue increased by 10%.",
        encoding="utf-8",
    )

    loader = MarkdownLoader()

    documents = loader.load(file_path)

    assert len(documents) == 1

    assert documents[0].content == (
        "# Financial Report\n\nRevenue increased by 10%."
    )

    assert documents[0].metadata["source"] == (
        str(file_path)
    )

    assert documents[0].metadata["type"] == "markdown"
