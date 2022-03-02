from pokedex_object import PokedexObject


class Move(PokedexObject):
    """
    Create Move class.
    """
    def __init__(self, name: int, pokedex_id: int, generation: str, accuracy: int, pp: int,
                 power: int, move_type: str, damage_class: str, effect_short: str):
        """
        Initialize params
        :param name: int
        :param pokedex_id: int
        :param generation: str
        :param accuracy: int
        :param pp: int
        :param power: int
        :param move_type: str
        :param damage_class: str
        :param effect_short: str
        """
        super().__init__(name, pokedex_id)
        self._generation = generation
        self._accuracy = accuracy
        self._pp = pp
        self._power = power
        self._move_type = move_type
        self._damage_class = damage_class
        self._effect_short = effect_short

    def __str__(self):
        return f"Name: {self.name}\n" \
               f"ID: {self.pokedex_id}\n" \
               f"Generation: {self._generation}\n" \
               f"Accuracy: {self._accuracy}\n" \
               f"PP: {self._pp}\n" \
               f"Power: {self._power}\n" \
               f"Type: {self._move_type}\n" \
               f"Damage Class: {self._damage_class}\n" \
               f"Effect (Short){self._effect_short}\n"
