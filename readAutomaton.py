def read_file(file_name):
    try:
        file = open(file_name,'r')
        file_strings = file.readlines()
        file.close()
        stringao = ''.join(file_strings)
        return stringao
    except:
        print(" File not found! Confirm if the input path is correct.\n")
        return -1


def read_automaton(definition_string):
    # Reading automata name
    stringao = definition_string
    stringao = stringao.replace(' ', '')

    automata_name = stringao[0:stringao.find('=')]
    stringao = stringao.removeprefix(automata_name + '={ {')
    stringao = stringao.removeprefix(automata_name + '={')  
    stringao = stringao.removeprefix('{')  
   
    # Extracting the automaton alphabet from file string
    alphabet_string = stringao[0:stringao.find('}')]
    alphabet_set = set(alphabet_string.split(','))
    stringao = stringao.removeprefix(alphabet_string + '},{')
    stringao = stringao.removeprefix(alphabet_string + '}, {')     
    stringao = stringao.removeprefix(alphabet_string + '},\n{')    

    # Extracting the automaton states from file string
    states_string = stringao[0:stringao.find('}')]
    states_list = states_string.split(',')
    states_list.sort()
    stringao = stringao.removeprefix(states_string + '}, ')     
    stringao = stringao.removeprefix(states_string + '},\n')
    stringao = stringao.removeprefix(states_string + '},') 

    # Extracting the automaton initial state from file string
    initial_state = stringao[0:stringao.find(',')]
    stringao = stringao.removeprefix(initial_state + ', {')
    stringao = stringao.removeprefix(initial_state + ',{')
    stringao = stringao.removeprefix(initial_state + ',\n{')
    initial_state_set = set([initial_state])

    # Extracting the automaton final states from file string
    final_states_string = stringao[0:stringao.find('}')]
    final_states_set = set(final_states_string.split(','))
    stringao = stringao.removeprefix(final_states_string + '} }\np:\n')
    stringao = stringao.removeprefix(final_states_string + '}}\np:\n')
    
    # Extracting the automaton productions from file string
    productions_string_list = stringao.split('\n')
    productions_list = []
    for production in productions_string_list:
        production = production.removeprefix('(')
        production = production.removesuffix(')')
        production_pieces = production.split(',')
        productions_list.append(production_pieces)
    productions_list.sort(key=lambda x:x[0])    
    
    # Creating dictionary for productions
    productions_dict = {}
    aux_dict = {}
    aux_list = []
    for production in productions_list:

        # Select a state
        origin_state = production[0]

        # Checks if the productions of that state were already catalogued
        if(origin_state not in productions_dict):

            # If not, creates a list with all the productions of that state
            for production in productions_list:
                if production[0] == origin_state:
                    aux_list.append(production)
            
            # Makes a dictionary with each transition as a key and destiny state as the answer
            for production in aux_list:
                transition = production[1]
                destiny = production[2]
                aux_dict[transition] = destiny

            # Adds the state that wasnt on the dictionary as a key with answer being its transition dictionary
            productions_dict[origin_state] = aux_dict
            aux_dict = {}
            aux_list = []

    return (alphabet_set, states_list, initial_state_set, final_states_set, productions_dict)




