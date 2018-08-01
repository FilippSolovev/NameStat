import ast
import os
import sys
from collections import Counter
from find_verbs import extract_verbs_from_funcname

import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')


def flatter_list(list_of_lists):
    output = []
    for sublist in list_of_lists:
        for item in sublist:
            output.append(item)
    return output


def fetch_list_of_fnames(path):
    list_of_fnames = []

    for dirname, dirs, files in os.walk(path, topdown=True):
        for fname in files:
            if fname.endswith('.py'):
                list_of_fnames.append(os.path.join(dirname, fname))
    logger.info(f'total {len(list_of_fnames)} files')
    return list_of_fnames


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
    logger.info('trees generated')
    return list_of_trees


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
    logger.info(f'total {len(output)} functions')
    return output


def find_frequent_verbs_within_path(path, head=10):
    list_of_func = fetch_list_of_func(path)

    verbs = []

    for function in list_of_func:
        verbs.append(extract_verbs_from_funcname(function))

    verbs = flatter_list(verbs)

    return Counter(verbs).most_common(head)


if __name__ == '__main__':

    TOP_SIZE = 10
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = '.'
    if not os.path.exists(path):
        logger.error('Path given does not exist.')
        sys.exit()

    verbs = find_frequent_verbs_within_path(path, head=TOP_SIZE)

    print('total %s words, %s unique' % (len(verbs), len(set(verbs))))

    for verb, occurence in verbs:
        print(verb, occurence)
