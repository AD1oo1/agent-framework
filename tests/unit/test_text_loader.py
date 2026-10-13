from pathlib import Path

from agent_framework.text_loader import TextLoader


def test_text_loader_loads_file(tmp_path: Path):

    file_path = tmp_path / "sample.txt"

    file_path.write_text(
        "Revenue increased by 10%.",
        encoding="utf-8",
    )

    loader = TextLoader()

    documents = loader.load(file_path)

    assert len(documents) == 1

    assert documents[0].content == (
        "Revenue increased by 10%."
    )

    assert documents[0].metadata["source"] == (
        str(file_path)
    )

    assert documents[0].metadata["type"] == "text"
