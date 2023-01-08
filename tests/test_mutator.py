import ast

from bamutpy import bamutpy_ast, mutator
from bamutpy.mutator import MutationType


FAKE_FILE_1_PATH = "/some/file/name.py"

FAKE_FILE_1_CODE = """
def compute(a, b):
    c = a *3
    return (a + c)

def main():
    compute(3, 2)
"""




class FakeScanner():

    def __init__(self, ast_tree_by_file):
        self._all_files = set(ast_tree_by_file.keys())
        self.ast_tree_by_file = ast_tree_by_file

    def all_files(self):
        return self._all_files



def test_basic_mutate():

    ast_tree = bamutpy_ast.parse_to_tree(ast.parse(FAKE_FILE_1_CODE))

    ast_tree_by_file = {FAKE_FILE_1_PATH: ast_tree}
    scanner = FakeScanner(ast_tree_by_file)

    remove_line_mutation = mutator.generate_mutations(scanner, amount=1, allowed_mutations=[MutationType.REMOVE_STATEMENT])[0]
    assert remove_line_mutation.mutation_type == MutationType.REMOVE_STATEMENT
    assert remove_line_mutation.file_path == FAKE_FILE_1_PATH
    assert remove_line_mutation.node_id == "Module.FunctionDef(0).Assign(2)"

