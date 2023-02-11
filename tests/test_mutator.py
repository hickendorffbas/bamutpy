import ast

from bamutpy import bamutpy_ast, mutator
from bamutpy.mutator import Mutation, MutationType


FAKE_FILE_1_PATH = "/some/file/name.py"
FAKE_FILE_1_CODE = """
def compute(a, b):
    c = a *3
    return (a + c)

def main():
    compute(3, 2)
"""

FAKE_FILE_2_PATH = "/some/other/file/name.py"
FAKE_FILE_2_CODE = """
def choose(option):
    to_return = ""
    if option == 1:
        to_return = "A"
    if option == 2:
        to_return = "B"
    return to_return
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



def test_remove_statement():

    ast_tree = bamutpy_ast.parse_to_tree(ast.parse(FAKE_FILE_2_CODE))
    ast_tree_by_file = {FAKE_FILE_2_PATH: ast_tree}
    scanner = FakeScanner(ast_tree_by_file)

    node_for_assignment_under_if = ast_tree.body[0].body[0]  #we take the assignment under the if to check if we insert a pass to not make the code invalid
    mutant_to_apply = Mutation(MutationType.REMOVE_STATEMENT, bamutpy_ast.node_id(node_for_assignment_under_if), -1)

    mutator.CodeTransformer(mutant_to_apply).visit(ast_tree)
    ast.fix_missing_locations(ast_tree)

    assert type(ast_tree.body[0].body[0]).__name__ == "Pass"


