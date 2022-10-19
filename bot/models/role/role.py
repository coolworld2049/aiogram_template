from dataclasses import dataclass


@dataclass
class UserRole:
    USER = "user"
    ADMIN = "admin"
    MANAGER = "manager"
