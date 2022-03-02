from pokedex_object import PokedexObject


class Stat(PokedexObject):
    """
    Create Stat class
    """
    def __init__(self, name: int, pokedex_id: int, is_battle_only: bool, move_damage_class=None):
        """
        Initialize params
        :param name: int
        :param pokedex_id: int
        :param is_battle_only: bool
        :param move_damage_class:
        """
        super().__init__(name, pokedex_id)
        self._is_battle_only = is_battle_only
        self._move_damage_class = move_damage_class

    def __str__(self):
        """
        Format Stat
        :return: str
        """
        if self._move_damage_class is None:
            self._move_damage_class = "N/A"
        return f"Name: {self.name}\n" \
               f"ID: {self.pokedex_id}\n" \
               f"Is_Battle_Only: {self._is_battle_only}\n" \
               f"Move Damage Class: {self._move_damage_class}\n"
