from pokedex_object import PokedexObject


class Pokemon(PokedexObject):
    """
    Create Pokemon class
    """

    def __init__(self, name: int, pokedex_id: int, height: int, weight, stats, types, abilities, moves: list):
        """
        Initialize params
        :param name: int
        :param pokedex_id: int
        :param height: int
        :param weight: int
        :param stats: string
        :param types: string
        :param abilities: lsit
        :param moves: list
        """
        super().__init__(name, pokedex_id)
        self._height = height
        self._weight = weight
        self._stats = stats
        self._abilities = abilities
        self._moves = moves
        self._types = types

    def __str__(self):
        """
        Format Pokemon
        :return: str
        """
        stats = '\n'.join((str(x)) for x in self._stats)
        abilities = '\n'.join(str(x) for x in self._abilities)
        moves = '\n'.join(str(x) for x in self._moves)
        return f"Name: {self.name}\n" \
               f"ID: {self.pokedex_id}\n" \
               f"Height: {self._height}\n" \
               f"Weight: {self._weight}\n" \
               f"Type: {''.join(self._types)}\n" \
               f"Stats:\n------\n\n{stats}\n"\
               f"Ability:\n------\n\n{abilities}\n" \
               f"Moves:\n------\n\n{moves}\n"

