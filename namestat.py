import ast
import os
import functools
import sys
from collections import Counter

from nltk import pos_tag


def inform_status(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        output = func(*args, **kwargs)
        func_name = parse_snake_case(func.__name__)
        if func_name[3] == 'fnames':
            print('total %s files' % len(output))
        if func_name[3] == 'trees':
            print('trees generated')
        if func_name[3] == 'func':
            print('total %s functions' % len(output))
        return output
    return wrapped


def flatter_a_list(list_of_lists):
    output = []
    for sublist in list_of_lists:
        for item in sublist:
            output.append(item)
    return output


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


@inform_status
def fetch_list_of_fnames(path):
    list_of_fnames = []

    for dirname, dirs, files in os.walk(path, topdown=True):
        for fname in files:
            if fname.endswith('.py'):
                list_of_fnames.append(os.path.join(dirname, fname))
                if len(list_of_fnames) == 100:
                    break
    return list_of_fnames


@inform_status
def fetch_list_of_trees(path):
    list_of_fnames = fetch_list_of_fnames(path)

    list_of_trees = []

    for fname in list_of_fnames:
        with open(fname, 'r', encoding='utf-8') as current_file:
            current_fcontent = current_file.read()
        try:
            tree = ast.parse(current_fcontent)
        except SyntaxError as error:
            print(error)
            continue
        list_of_trees.append(tree)

    return list_of_trees


@inform_status
def fetch_list_of_func(path):
    list_of_trees = fetch_list_of_trees(path)

    list_of_func = []

    for tree in list_of_trees:
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                list_of_func.append(node.name.lower())

    output = []

    for function in list_of_func:
        if not (function.startswith('__') and function.endswith('__')):
            output.append(function)

    return output


def parse_snake_case(sc_name):
    return [word for word in sc_name.split('_') if word]


def extract_verbs_from_funcname(function_name):
    words = parse_snake_case(function_name)
    return [word for word in words if is_verb(word)]


def find_frequent_verbs_within_path(path, head=10):
    list_of_func = fetch_list_of_func(path)

    verbs = []

    for function in list_of_func:
        verbs.append(extract_verbs_from_funcname(function))

    verbs = flatter_a_list(verbs)

    return Counter(verbs).most_common(head)


def main():

    TOP_SIZE = 10
    try:
        path = sys.argv[1]
    except IndexError as error:
        path = '.'

    verbs = find_frequent_verbs_within_path(path, head=TOP_SIZE)

    print('total %s words, %s unique' % (len(verbs), len(set(verbs))))

    for verb, occurence in verbs:
        print(verb, occurence)


if __name__ == '__main__':
    main()
