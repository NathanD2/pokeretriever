import asyncio, aiohttp
from pokemon import Pokemon
from move import Move
from poke_stat import Stat
from ability import Ability


class FetchPokedexObject:
    """
    Represents a FetchPoketex Object.
    """

    base_url = "https://pokeapi.co/api/v2/{ext}/{id}"

    @classmethod
    def executes_requests(cls, mode: str, requests: list, extension: bool = False):
        """
        Executes requests.
        :param mode: a str
        :param requests: a list
        :param extension: a bool
        :return: a list
        """
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(FetchPokedexObject.executes_requests_helper(mode, requests, extension))

        if extension:
            pokedex_objects = FetchPokedexObject.retrieve_pokedex_objects_extended(response)

        else:
            pokedex_objects = cls.retrieve_pokedex_objects(mode, response)
        return pokedex_objects

    @classmethod
    async def executes_requests_helper(cls, mode: str, requests: list, extension: bool = False):
        async with aiohttp.ClientSession() as session:
            async_coroutines = [cls.query_pokedex_information(session, mode, request[0], request[1])
                                for request in requests]

            responses = await asyncio.gather(*async_coroutines)

            return responses

    @classmethod
    async def query_pokedex_information(cls, session, url_ext: str = None, name=None, pokedex_id=None, url_full=None):
        """
        Queries pokedex information.
        :param session: a session
        :param url_ext: a str
        :param name: a str
        :param pokedex_id: an int
        :param url_full: a str
        :return: a dict
        """
        if url_full is not None:
            target_url = url_full
        elif name is None:
            target_url = cls.base_url.format(ext=url_ext, id=pokedex_id)
        else:
            target_url = cls.base_url.format(ext=url_ext, id=name)
        response = await session.request(method="GET", url=target_url)
        try:
            json_dict = await response.json()
        except aiohttp.ContentTypeError:
            return "An error occurred. Skipping this request.\n\n"
        return json_dict

    @classmethod
    def retrieve_pokedex_objects(cls, mode, responses):
        """
        Retrieves pokedex objects.
        :param mode: a str
        :param responses: a list
        :return: a list
        """
        pokedex_objects = []
        extras = {}
        if mode == 'pokemon':
            for response in responses:
                extras['abilities'] = [ability['ability']['name'] for ability in
                                       response['abilities']]
                extras['stats'] = [(stat['stat']['name'], stat['base_stat']) for stat in response['stats']]
                extras['moves'] = [(move['move']['name'], move['version_group_details'][0]['level_learned_at']) for move in response['moves']]

                types = [pokemon_type['type']['name'] for pokemon_type in response['types']]

                pokedex_objects.append(Pokemon(response['name'],
                                               response['id'],
                                               response['height'],
                                               response['weight'],
                                               abilities=extras['abilities'],
                                               types=types,
                                               stats=extras['stats'],
                                               moves=extras['moves'],

                                               ))
        elif mode == 'ability':
            pokedex_objects = cls.generate_ability_list(responses)

        elif mode == 'move':
            pokedex_objects = cls.generate_move_list(responses)

        return pokedex_objects

    @classmethod
    def generate_ability_list(cls, responses):
        """
        Generates list of abilities.
        :param responses: a list
        :return: a list
        """
        abilities = []
        for response in responses:
            if isinstance(response, str):
                abilities.append(response)
                continue
            name = response['name']
            pokedex_id = response['id']
            gen = response['generation']['name']
            effect = response['effect_entries'][1]['effect']
            effect_short = response['effect_entries'][1]['short_effect']
            pokemon = [pokemon['pokemon']['name'] for pokemon in response['pokemon']]
            abilities.append(Ability(name, pokedex_id, gen, effect, effect_short, pokemon))
        return abilities

    @classmethod
    def generate_move_list(cls, responses):
        """
        Generates list of moves.
        :param responses: a list
        :return: a list
        """
        move_list = []
        for response in responses:
            if isinstance(response, str):
                move_list.append(response)
                continue
            name = response['name']
            pokedex_id = response['id']
            gen = response['generation']['name']
            accuracy = response['accuracy']
            pp = response['pp']
            power = response['power']
            move_type = response['type']['name']
            damage_class = response['damage_class']['name']
            effect_short = None
            for effect in response['effect_entries']:
                if effect['language']['name'] == "en":
                    effect_short = effect['short_effect']
                    break
            temp = Move(name, pokedex_id, gen, accuracy, pp,
                        power, move_type, damage_class, effect_short)
            move_list.append(temp)
        return move_list

    @classmethod
    def generate_stat_list(cls, responses):
        """
        Generates stats list.
        :param responses: a list
        :return: a list
        """
        stat_list = []
        for response in responses:
            if isinstance(response, str):
                stat_list.append(response)
                continue
            name = response['name']
            pokedex_id = response['id']
            is_battle_only = response['is_battle_only']
            temp = Stat(name, pokedex_id, is_battle_only)
            stat_list.append(temp)
        return stat_list

    @classmethod
    def retrieve_pokedex_objects_extended(cls, responses):
        """
        Retrieves pokedex objects for extended functionality.
        :param responses: a list
        :return: a list
        """
        pokedex_objects = []
        for pokemon in responses:
            if isinstance(pokemon, str):
                pokedex_objects.append(pokemon)
                continue
            # async with aiohttp.ClientSession() as session:
            stat_urls = [stat['stat']['url'] for stat in pokemon['stats']]
            move_urls = [move['move']['url'] for move in pokemon['moves']]
            ability_urls = [ability['ability']['url'] for ability in pokemon['abilities']]

            types = [pokemon_type['type']['name'] for pokemon_type in pokemon['types']]

            loop = asyncio.get_event_loop()
            stat_responses = loop.run_until_complete(FetchPokedexObject.retrieve_pokedex_objects_extended_helper(stat_urls))
            move_responses = loop.run_until_complete(FetchPokedexObject.retrieve_pokedex_objects_extended_helper(move_urls))
            ability_responses = loop.run_until_complete(FetchPokedexObject.retrieve_pokedex_objects_extended_helper(ability_urls))

            pokedex_objects.append(Pokemon(pokemon['name'],
                                           pokemon['id'],
                                           pokemon['height'],
                                           pokemon['weight'],
                                           cls.generate_stat_list(stat_responses),
                                           types,
                                           cls.generate_ability_list(ability_responses),
                                           cls.generate_move_list(move_responses)
                                           ))

        return pokedex_objects

    @classmethod
    async def retrieve_pokedex_objects_extended_helper(cls, stat_urls):
        async with aiohttp.ClientSession() as session:
            async_coroutines = [cls.query_pokedex_information(session, url_full=url)
                                for url in stat_urls]
            responses = await asyncio.gather(*async_coroutines)
            return responses
