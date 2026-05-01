from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class Category:
    id: int = 0
    name: str = ""


@dataclass
class Tag:
    id: int = 0
    name: str = ""


@dataclass
class Pet:
    name: str
    photoUrls: List[str]
    id: int = 0
    category: Category = field(default_factory=Category)
    tags: List[Tag] = field(default_factory=list)
    status: str = "available"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "category": asdict(self.category),
            "name": self.name,
            "photoUrls": self.photoUrls,
            "tags": [asdict(t) for t in self.tags],
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Pet":
        category_data = data.get("category") or {}
        tags_data = data.get("tags") or []
        return cls(
            id=data.get("id", 0),
            name=data["name"],
            photoUrls=data.get("photoUrls", []),
            category=Category(**category_data) if category_data else Category(),
            tags=[Tag(**t) for t in tags_data],
            status=data.get("status", "available"),
        )
