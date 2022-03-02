import argparse
from request_handler import *
class Request:
    """
    Create Request class to create request format.
    """

    def __init__(self):
        """
        Initialize params.
        """
        self._mode = None
        self._input_file = None
        self._input_data = None
        self._expanded = None
        self._output = None
        self._data_collection = list()
        self._output_list = None

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    @property
    def input_file(self):
        return self._input_file

    @input_file.setter
    def input_file(self, input_file):
        self._input_file = input_file

    @property
    def input_data(self):
        return self._input_data

    @input_data.setter
    def input_data(self, input_data):
        self._input_data = input_data

    @property
    def expanded(self):
        return self._expanded

    @expanded.setter
    def expanded(self, expanded):
        self._expanded = expanded

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, output):
        self._output = output

    @property
    def data_collection(self):
        return self._data_collection

    @data_collection.setter
    def data_collection(self, data_collection):
        self._data_collection = data_collection

    @property
    def output_list(self):
        return self._output_list

    @output_list.setter
    def output_list(self, output_list):
        self._output_list = output_list

    def __str__(self):
        """
        String the request info.
        :return: str
        """
        return f"{self.mode} {self.expanded} {self.input_data} {self.input_file} {self.output} {self.data_collection}"



class Pokedex:
    """
    Create Pokedex class to accept params in terminal and execute the command.
    """

    def __init__(self):
        """
        Initialize params.
        """
        self.parser = argparse.ArgumentParser()
        self.request = Request()

    def setup_request_commandline(self):
        """
        Setup parser and save the input in request.
        """
        parser = self.parser
        group_input = parser.add_mutually_exclusive_group()
        group_input.add_argument("--inputfile", help="The file is txt file")
        group_input.add_argument("--inputdata", help="The input data can be name or ID")
        parser.add_argument("--output", default="print", help="To check to expand tha data or not")
        parser.add_argument("mode", help="the input will be an id or the name of a pokemon, ability or move.")
        parser.add_argument("--expanded", action="store_true", default=False, help="To check to expand tha data or not")

        try:
            request = self.request
            args = parser.parse_args()
            request.input_file = args.inputfile
            request.input_data = args.inputdata
            request.mode = args.mode
            request.output = args.output
            request.expanded = args.expanded
            return request

        except Exception as e:
            print(f"Error! Could not read arguments.\n{e}")
            quit()


class PokedexProcess:
    """
    Create PokedexProcess to handle the handlers to check format is correct or not.
    """

    def __init__(self):
        mode_handler = ModeHandler()
        input_file_data_handler = InputFileDataHandler()
        expanded_handler = ExpandedHandler()
        output_handler = OutputHandler()

        # whole setup
        mode_handler.set_handler(input_file_data_handler)
        input_file_data_handler.set_handler(expanded_handler)
        expanded_handler.set_handler(output_handler)
        self.handler_chain_head_whole = mode_handler

    def execute_request(self, request: Request):
        """
        Check te request is successfully go though all handlers.
        :param request: Request
        """
        result = self.handler_chain_head_whole.handle_request(request)
        if result[1]:
            print("Success finish the handler")
        else:
            print(result[0])


def main(request: Request = None):
    """
    Run main
    """
    facade = PokedexProcess()
    facade.execute_request(request)


if __name__ == '__main__':
    pokedex = Pokedex()
    request = pokedex.setup_request_commandline()
    main(request)
