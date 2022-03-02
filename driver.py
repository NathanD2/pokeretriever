from pokedex import Pokedex, PokedexProcess, Request

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
