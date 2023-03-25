from dataclasses import dataclass, field

@dataclass
class Channel:
    id: str
    name: str
    tags: list[str] = field(default_factory=list)
    description: str = ""
