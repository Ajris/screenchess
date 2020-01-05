from dataclasses import dataclass
from .color import Color


@dataclass
class Piece:
    x: int
    y: int
    color: Color
