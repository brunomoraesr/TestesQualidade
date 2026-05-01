from dataclasses import dataclass, asdict, field


@dataclass
class User:
    username: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: str
    id: int = 0
    userStatus: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        return cls(
            id=data.get("id", 0),
            username=data["username"],
            firstName=data.get("firstName", ""),
            lastName=data.get("lastName", ""),
            email=data.get("email", ""),
            password=data.get("password", ""),
            phone=data.get("phone", ""),
            userStatus=data.get("userStatus", 0),
        )
