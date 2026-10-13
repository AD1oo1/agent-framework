from dataclasses import dataclass, field


@dataclass
class DocumentChunk:
    content: str

    metadata: dict = field(
        default_factory=dict
    )
