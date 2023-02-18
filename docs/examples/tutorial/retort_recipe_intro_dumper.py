from dataclasses import dataclass
from datetime import datetime

from adaptix import Retort, dumper, loader


@dataclass
class Book:
    title: str
    price: int
    created_at: datetime


data = {
    "title": "Fahrenheit 451",
    "price": 100,
    "created_at": 1674938508.599962,
}

retort = Retort(
    recipe=[
        loader(datetime, datetime.fromtimestamp),
        dumper(datetime, datetime.timestamp),
    ],
)

book = retort.load(data, Book)
assert book == Book(
    title="Fahrenheit 451",
    price=100,
    created_at=datetime(2023, 1, 28, 23, 41, 48, 599962),
)
assert retort.dump(book) == data