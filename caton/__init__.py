import random
from enum import Enum
from typing import ClassVar

from pydantic import BaseModel


class Model(BaseModel, extra="forbid"):
    pass


class Resource(Model):
    name: str


WOOD = Resource(name="wood")
BRICK = Resource(name="brick")
ORE = Resource(name="ore")
GRAIN = Resource(name="grain")
WOOL = Resource(name="wool")
NOTHING = Resource(name="nothing")


class Terrain(Model):
    name: str
    resource: Resource


HILLS = Terrain(name="Hills", resource=BRICK)
MOUNTAINS = Terrain(name="Mountains", resource=ORE)
FIELDS = Terrain(name="Fields", resource=GRAIN)
FOREST = Terrain(name="Forest", resource=WOOD)
PASTURE = Terrain(name="Pasture", resource=WOOL)
DESERT = Terrain(name="Desert", resource=NOTHING)
WATER = Terrain(name="Water", resource=NOTHING)

class NumberToken(Model):
    value: int | None

class HexLocation(Model):
    # https://www.redblobgames.com/grids/hexagons/
    q: int
    r: int
    s: int

    def __post_init__(self):
        if self.q + self.r + self.s != 0:
            raise ValueError(f"{self.q=} + {self.r=} + {self.s=} = {self.q+self.r+self.s} != 0")

    @classmethod
    def from_x_y(cls, x: int, y: int) -> "HexLocation":
        return cls(q=x-y, r=y, s=-x)

class Hex(Model):
    terrain: Terrain
    number_token: NumberToken
    location: HexLocation

class Harbour(Model):
    resource: Resource

class BoardLayout(Model):
    n_players: int = 4
    hexes: list[Hex]


def _terrains_by_player(n_players: int) -> int:
    if n_players < 1:
        raise ValueError(f"{n_players=} must be at least 1")
    if n_players < 5:
        return (
            (MOUNTAINS, 3),
            (HILLS, 3),
            (FOREST, 4),
            (FIELDS, 4),
            (PASTURE, 4),
            (DESERT, 1),
        )
    if n_players < 7:
        return (
            (MOUNTAINS, 5),
            (HILLS, 5),
            (FOREST, 6),
            (FIELDS, 6),
            (PASTURE, 6),
            (DESERT, 2),
        )
    raise ValueError(f"Too many players {n_players}")


def _counters_by_players(n_players: int) -> list[int | None]:
    """
    7's are represented as None as no counters should go on the desert
    """
    if n_players < 1:
        raise ValueError(f"{n_players=} must be at least 1")
    elif n_players > 6:
        raise ValueError(f"{n_players=} must be at most 6")

    if n_players < 5:
        default_num = 1
    else:
        default_num = 2

    counters = []
    for i in range(2, 13):
        if i == 7:
            counters.extend([None] * default_num)
            continue
        counters.extend([i] * default_num)
        if i not in (2, 12):
            counters.append(i)
    return counters


def _list_breaks_by_players(n_players: int) -> list[int]:
    if n_players < 1:
        raise ValueError(f"{n_players=} must be at least 1")
    if n_players < 5:
        return [0, 3, 7, 12, 16, 19]
    if n_players < 7:
        return [0, 3, 7, 12, 18, 23, 27, 30]
    raise ValueError(f"Too many players {n_players}")


def _split_list_to_board(data: list, n_players: int) -> list[list]:
    breaks = _list_breaks_by_players(n_players)
    board = []
    for start, end in zip(breaks[:-1], breaks[1:], strict=True):
        board.append(data[start:end])
    return board

def generate_random_board_layout(n_players: int = 4) -> BoardLayout:
    terrains = generate_random_terrains(n_players)
    hexes = _generate_hexes_from_terrains(n_players, terrains)
    return BoardLayout(n_players=n_players, hexes=hexes)


def generate_random_terrains(
    n_players: int = 4, *, serialised: bool = False
) -> list[list[Terrain]]:
    hexes = [hex for hex, n in _terrains_by_player(n_players) for _ in range(n)]
    random.shuffle(hexes)
    result = _split_list_to_board(hexes, n_players)
    if serialised:
        result = [[hex.name for hex in row] for row in result]
    return result


def _generate_hexes_from_terrains(n_players: int, terrains: list[list[Terrain]]) -> list[Hex]:
    number_tokens = _counters_by_players(n_players)
    random.shuffle(number_tokens)
    hexes = []
    for y, row in enumerate(terrains):
        for x, terrain in enumerate(row):
            if terrain.resource == NOTHING:
                token = None
            else:
                token = number_tokens.pop()
            hex = Hex(terrain=terrain, location=HexLocation.from_x_y(x, y), number_token=NumberToken(token))
            hexes.append(hex)
    return hexes
