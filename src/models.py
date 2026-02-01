from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorites_characters = Table(
    "favorites_characters",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)

favorites_locations = Table(
    "favorites_locations",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("location_id", ForeignKey("location.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    favorites_characters: Mapped[list["Character"]] = db.relationship(
        "Character",
        secondary = favorites_characters,
        back_populates = "favorited_by_user"
    )
    favorites_locations: Mapped[list["Location"]] = db.relationship(
        "Location",
        secondary = favorites_locations,
        back_populates = "favorited_by_user"
    )

    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_characters": [character.serialize() for character in self.favorites_characters],
            "favorite_locations": [location.seralize() for location in self.favorites_locations],
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    age: Mapped[int] = mapped_column(Integer)
    ocupation: Mapped[str] = mapped_column(String(120))
    favorited_by_user: Mapped[list["User"]] = db.relationship(
        "User",
        secondary = favorites_characters,
        back_populates = "favorites_characters"
    )
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "ocupation": self.ocupation
        }
    

class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    town: Mapped[str] = mapped_column(String(50))
    use: Mapped[str] = mapped_column(String(50))

    favorited_by_user: Mapped[list["User"]] = db.relationship(
        "User",
        secondary = favorites_locations,
        back_populates = "favorites_locations"
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'town': self.town,
            'use': self.use
        }
