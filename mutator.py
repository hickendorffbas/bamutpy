import ast
import random

from enum import Enum

from bamutpy import bamutpy_ast


class MutationType(Enum):
    SWAP_OPERATOR = 1
    SWAP_EQ_NEQ = 2
    REMOVE_STATEMENT = 3


class Mutation:

    def __init__(self, mutation_type, node_id, line_number, change_data=None):
        self.mutation_type = mutation_type
        self.change_data = change_data
        self.node_id = node_id
        self.line_number = line_number
        self.file_path = None

    def __str__(self):
        return f"<Mutation {self.mutation_type}, {self.change_data}, {self.node_id}, {self.file_path}:{self.line_number}>"

    def applies_to(self, node, mutation_type):
        return (self.node_id == bamutpy_ast.node_id(node)) and (mutation_type == mutation_type)


class MutantGenerator(ast.NodeVisitor):

    def __init__(self, allowed_mutations=None):
        self.potential_mutants = set()
        self.allowed_mutations = allowed_mutations

    def visit_Eq(self, node):
        self._add_mutation(Mutation(MutationType.SWAP_EQ_NEQ, bamutpy_ast.node_id(node), bamutpy_ast.find_line_number(node)))
        self.generic_visit(node)

    def visit_NotEq(self, node):
        self._add_mutation(Mutation(MutationType.SWAP_EQ_NEQ, bamutpy_ast.node_id(node), bamutpy_ast.find_line_number(node)))
        self.generic_visit(node)

    def visit_Add(self, node):
        self._add_swap_operator_mutation_except(node, "+")
        self.generic_visit(node)

    def visit_Sub(self, node):
        self._add_swap_operator_mutation_except(node, "-")
        self.generic_visit(node)

    def visit_Mult(self, node):
        self._add_swap_operator_mutation_except(node, "*")
        self.generic_visit(node)

    def visit_Div(self, node):
        self._add_swap_operator_mutation_except(node, "/")
        self.generic_visit(node)

    def visit_Assign(self, node):
        self._add_remove_statement_mutation(node)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        self._add_remove_statement_mutation(node)
        self.generic_visit(node)

    def _add_remove_statement_mutation(self, node):
        self._add_mutation( Mutation(MutationType.REMOVE_STATEMENT, bamutpy_ast.node_id(node), bamutpy_ast.find_line_number(node)) )

    def _add_swap_operator_mutation_except(self, node, operator_to_skip):
        for operator in ("+", "-", "*", "/"):
            if operator != operator_to_skip:
                self._add_mutation(Mutation(MutationType.SWAP_OPERATOR, bamutpy_ast.node_id(node), bamutpy_ast.find_line_number(node), change_data=operator))

    def _add_mutation(self, mutation):
        if self.allowed_mutations and mutation.mutation_type not in self.allowed_mutations:
            return

        self.potential_mutants.add(mutation)



class CodeTransformer(ast.NodeTransformer):

    def __init__(self, mutation):
        self._mutation = mutation

    def visit_Eq(self, node):
        if self._mutation.applies_to(node, MutationType.SWAP_EQ_NEQ):
            return ast.NotEq()
        return node

    def visit_NotEq(self, node):
        if self._mutation.applies_to(node, MutationType.SWAP_EQ_NEQ):
            return ast.Eq()
        return node

    def visit_Add(self, node):
        if self._mutation.applies_to(node, MutationType.SWAP_OPERATOR):
            return self._get_node_for_operator(self._mutation.change_data)
        return node

    def visit_Sub(self, node):
        if self._mutation.applies_to(node, MutationType.SWAP_OPERATOR):
            return self._get_node_for_operator(self._mutation.change_data)
        return node

    def visit_Mult(self, node):
        if self._mutation.applies_to(node, MutationType.SWAP_OPERATOR):
            return self._get_node_for_operator(self._mutation.change_data)
        return node

    def visit_Div(self, node):
        if self._mutation.applies_to(node, MutationType.SWAP_OPERATOR):
            return self._get_node_for_operator(self._mutation.change_data)
        return node

    def visit_Assign(self, node):
        if self._mutation.applies_to(node, MutationType.REMOVE_STATEMENT):
            return None
        return node

    def visit_AugAssign(self, node):
        if self._mutation.applies_to(node, MutationType.REMOVE_STATEMENT):
            return None
        return node

    def _get_node_for_operator(self, operator):
        if operator == "+":
            return ast.Add()
        if operator == "-":
            return ast.Sub()
        if operator == "*":
            return ast.Mult()
        if operator == "/":
            return ast.Div()
        raise Exception("Unknown operator to change to: " + str(self._change_data))


def generate_mutations(scanner, amount=1, allowed_mutations=None): #TODO: enable setting allowed_mutations from the config file (as enum names....)

    all_mutations = []
    for file_path in scanner.all_files():
        generator = MutantGenerator(allowed_mutations)
        generator.visit(scanner.ast_tree_by_file[file_path])

        for potential_mutant in generator.potential_mutants:
            potential_mutant.file_path = file_path

        all_mutations.extend(generator.potential_mutants)

    if len(all_mutations) < amount:
        raise Exception(f"There are not enough possible mutations to find {amount}")

    random.shuffle(all_mutations)
    return all_mutations[0:amount]


