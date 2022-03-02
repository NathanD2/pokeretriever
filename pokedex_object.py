import abc

class PokedexObject(abc.ABC):
    """
    Represents a Pokedex abstract object.
    """

    def __init__(self, name: int, pokedex_id: int):
        """
        Initializes a concrete PokeDex Object Object.
        :param name: a str
        :param pokedex_id: an int
        """
        self._name = name
        self._pokedex_id = pokedex_id

    @property
    def name(self):
        """
        Gets name.
        :return: a str
        """
        return self._name

    @property
    def pokedex_id(self):
        """
        Gets pokedex ID.
        :return: an int
        """
        return self._pokedex_id

