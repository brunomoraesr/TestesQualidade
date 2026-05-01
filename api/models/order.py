from dataclasses import dataclass, asdict


@dataclass
class Order:
    petId: int
    quantity: int
    id: int = 0
    shipDate: str = ""
    status: str = "placed"
    complete: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        return cls(
            id=data.get("id", 0),
            petId=data["petId"],
            quantity=data.get("quantity", 1),
            shipDate=data.get("shipDate", ""),
            status=data.get("status", "placed"),
            complete=data.get("complete", False),
        )
