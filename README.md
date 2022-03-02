***British Columbia Institute of Technology - Computer Systems Technology Assignment***

Term 3 - COMP 3522 - Co-written with a classmate (Tommy Chien)

PokeRetriever
-
Uses Object-Oriented programming with command-line parsing for asynchronous HTTP requests to PokeAPI. API data transformed into Python objects with information presented via console or output txt file.
<br />
API Information: https://pokeapi.co/docs/v2 <br /><br />
***How to use***

py pokedex.py {"pokemon" | "ability" | "move"} {--inputfile "filename.txt" |--inputdata "name
or id"} [--expanded] [--output "filename.txt"]

** ensure current directory in /pokeretriever<br />
** python3 instead of py on Mac OS<br />
** input data for queries can be ID's or strings (ex: "pikachu" or 25)<br />
** input files can call multiple queries asynchronously<br />
** --expanded Default is False and only Pokemon queries can be expanded<br />
** --output Default is "print" (to console)<br />
** Included .txt input files can be used to interact with the application.<br />

***Test Commands***<br /><br/>
py pokedex.py pokemon --inputfile input_pokemon.txt
- _Pokemon information printed to the console_<br/><br/>

py pokedex.py ability --inputfile input_ability.txt --output output.txt
- _Ability information written to output.txt. Similar to expected output output_ability.txt_<br/><br/>

py pokedex.py move --inputdata 5
- _Input data through command line and Move information printed to the console_<br/><br/>

py pokedex.py pokemon --inputfile input_pokemon.txt --expanded --output output.txt
- _output.txt will be similar to output_pokemon_expand.txt_


Development Notes
-
PokeRetriever was co-written with a classmate (Tommy Chien) for an Assignment during Term 3 of the CST. I did not contribute to the command-line parsing part of the program mostly contained in pokedex.py