from nltk import pos_tag


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    verbs = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
    return True if pos_info[0][1] in verbs else False


def parse_snake_case(sc_name):
    return [word for word in sc_name.split('_') if word]


def extract_verbs_from_funcname(function_name):
    words = parse_snake_case(function_name)
    return [word for word in words if is_verb(word)]
