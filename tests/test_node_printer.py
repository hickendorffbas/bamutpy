import ast
import inspect


from bamutpy.node_printer import node_to_string


def function_for_test():
    amount = 1 + 3 * sum([1,2,3])
    print(amount)


def test_format_function():
    tree = ast.parse(inspect.getsource(function_for_test))
    nodes = tree.body[0].body

    assert len(nodes) == 2

    node_0_str = node_to_string(nodes[0])    
    assert node_0_str == """<Assign: ['<Name: amount>'] <BinOp: <Add> <Constant: 1> <BinOp: <Mult> <Constant: 3> <Call: <Name: sum> ["<List: ['<Constant: 1>', '<Constant: 2>', '<Constant: 3>']>"]>>>>"""

    node_1_str = node_to_string(nodes[1])    
    assert node_1_str == """<Expr: <Call: <Name: print> ['<Name: amount>']>>"""

