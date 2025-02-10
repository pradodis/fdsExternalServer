class bcolors:
    HEADER = "\033[95m"
    BLUE = "\033[34m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    PURPLE = "\033[35m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

coalition_code_ingame = {
    '0': 'neutral',
    '1': 'blue',
    '2': 'red'
}

coalition_code_network = {
    '1': 'neutral',
    '3': 'blue',
    '2': 'red'
}

grpc_coalition_enum = {
    'blue': 'COALITION_BLUE',
    'red': 'COALITION_RED'
}

grpc_object_category = {
    '0': 'player',
    '1': 'airplane',
    '2': 'helicopter',
    '3': 'ground',
    '4': 'ship'
}