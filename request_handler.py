import abc
import enum
from enum import auto
from fetch_pokedex_object import FetchPokedexObject
from datetime import datetime


class PokemonMode(enum.Enum):
    """
    Create PokemonMode enum to check mode.
    """
    POKEMON = auto()
    ABILITY = auto()
    MOVE = auto()

    @classmethod
    def has_name(cls, name):
        """
        If the name is POKEMON, ABILITY or MOVE
        :param name: str
        :return: bool
        """
        return name.strip().upper() in cls._member_names_


class RequestHandler(abc.ABC):
    """
    Create RequestHandler Abstract class.
    """

    def __init__(self, next_handler=None):
        """
        Initialize params
        :param next_handler: Request
        """
        self.next_handler = next_handler

    @abc.abstractmethod
    def handle_request(self, request) -> (str, bool):
        """
        Handle request
        :param request: Request
        """
        pass

    def set_handler(self, handler) -> (str, bool):
        """
        Set handler
        :param handler: Handler
        """
        self.next_handler = handler


class ModeHandler(RequestHandler):
    """
    Create ModeHandler class
    """
    def handle_request(self, request) -> (str, bool):
        """
        Handle request
        :param request: Request
        :return: tuple or request
        """
        if request.mode is not None:
            if PokemonMode.has_name(request.mode):
                return self.next_handler.handle_request(request)
            else:
                return "The Pokedex only provide the modes below: Pokemon, Ability and Move. ", False


class InputFileDataHandler(RequestHandler):
    """
    Create InputFileDataHandler class
    """
    def handle_request(self, request) -> (str, bool):
        """
        Handle request
        :param request: Request
        :return: tuple or request
        """
        input_file = request.input_file
        input_data = request.input_data
        if input_file is not None and input_data is None:
            file_names = input_file.strip().split(".")
            if len(file_names) == 2 and file_names[1] == "txt":
                self.read_file_helper(input_file, request)
                if not self.next_handler:
                    return "", True
                return self.next_handler.handle_request(request)
            else:
                return "We only process file name with txt format", False
        elif input_file is None and input_data is not None:
            request.data_collection.append(
                [None, input_data]) if input_data.isdecimal() else request.data_collection.append([input_data, None])
            if not self.next_handler:
                return "", True
            return self.next_handler.handle_request(request)
        else:
            return "A least need a input file or input data", False

    @staticmethod
    def read_file_helper(input_file, request):
        """
        Read file
        :param input_file: name
        :param request: Request
        """
        with open(input_file, mode='r', encoding='utf-8') as content:
            text = content.read()
            collections = text.split("\n")
            for cata in collections:
                request.data_collection.append([None, cata]) if cata.isdecimal() else request.data_collection.append(
                    [cata, None])


class ExpandedHandler(RequestHandler):
    """
    Create ExpandedHandler class
    """
    def handle_request(self, request) -> (str, bool):
        """
        Handle expanded request
        :param request: Request
        :return: tuple or request
        """
        expanded = request.expanded
        if expanded and request.mode != "pokemon":
            return "Only pokemon can do expanded", False
        else:
            self.save_mode_helper(request, expanded)
        if not self.next_handler:
            return "", True
        else:
            return self.next_handler.handle_request(request)

    @staticmethod
    def save_mode_helper(request, expanded):
        """
        Save the mode.
        :param request: Request
        :param expanded: bool
        """
        request.output_list = FetchPokedexObject.executes_requests(request.mode, request.data_collection, expanded)


class OutputHandler(RequestHandler):
    """
    Create OutputHandler class
    """
    def handle_request(self, request) -> (str, bool):
        """
        Handle output request
        :param request: Request
        :return: tuple or request
        """
        output = request.output
        file_names = output.strip().split(".")
        data_result = request.output_list
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M")
        data_result.insert(0, f"Timestamp: {dt_string}\n")
        data_result.insert(1, f"Number of requests: {len(request.data_collection)}\n\n")
        if len(file_names) == 2 and file_names[1] == "txt":
            self.write_file_helper(output, data_result)
            if not self.next_handler:
                return "", True
            return self.next_handler.handle_request(request)
        elif output == "print":
            for index in data_result:
                print(index)
            if not self.next_handler:
                return "", True
            return self.next_handler.handle_request(request)
        else:
            return "We only process output file name with txt format", False

    @staticmethod
    def write_file_helper(output, data_result):
        """
        Write file.
        :param output: str
        :param data_result: list
        """
        with open(output, mode='w', encoding='utf-8') as content:
            content.write(''.join(str(x) for x in data_result))
