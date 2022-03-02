from pokedex_object import PokedexObject


class Ability(PokedexObject):
    """
    Create Ability class
    """

    def __init__(self, name: int, pokedex_id: int, generation: str, effect: str, effect_short: str, pokemon: list):
        """
        Initialize params
        :param name: int
        :param pokedex_id: int
        :param generation: str
        :param effect: str
        :param effect_short: str
        :param pokemon: list
        """
        super().__init__(name, pokedex_id)
        self._generation = generation
        self._effect = effect
        self._effect_short = effect_short
        self._pokemon = pokemon

    def __str__(self):
        """
        Format Ability
        :return: str
        """
        return f"Name: {self.name}\n" \
               f"ID: {self.pokedex_id}\n" \
               f"Generation: {self._generation}\n" \
               f"Effect: {self._effect}\n" \
               f"Effect (Short): {self._effect_short}\n" \
               f"Pokemon: {', '.join(str(x) for x in self._pokemon)}\n"

