import ast


def node_to_string(node):
    if isinstance(node, ast.Name):
        return f"<Name: {node.id}>"
    if isinstance(node, ast.Constant):
        return f"<Constant: {node.value}>"

    if isinstance(node, ast.BinOp):
        return f"<BinOp: {node_to_string(node.op)} {node_to_string(node.left)} {node_to_string(node.right)}>"

    if isinstance(node, ast.Expr):
        return f"<Expr: {node_to_string(node.value)}>"
    if isinstance(node, ast.Assign):
        return f"<Assign: {_list_to_string(node.targets)} {node_to_string(node.value)}>"

    if isinstance(node, ast.Call):
        return f"<Call: {node_to_string(node.func)} {_list_to_string(node.args)}>"
    if isinstance(node, ast.arg):
        return f"<Arg: {node_to_string(node.arg)}>"

    if isinstance(node, ast.ClassDef):
        return f"<ClassDef: {node.name}>"

    if isinstance(node, ast.ListComp):
        return f"<ListComp: {node_to_string(node.elt)}, {_list_to_string(node.generators)}>"
    if isinstance(node, ast.comprehension):
        return f"<Comprehension: {node_to_string(node.target)}, {node_to_string(node.iter)}>"

    if isinstance(node, ast.List):
        return f"<List: {_list_to_string(node.elts)}>"
    if isinstance(node, ast.Tuple):
        return f"<Tuple: {_list_to_string(node.elts)}>"

    if isinstance(node, ast.Import):
        return f"<Import: {_list_to_string(node.names)}>"
    if isinstance(node, ast.ImportFrom):
        return f"<ImportFrom: {node.module}, {_list_to_string(node.names)}, {node.level}>"
    if isinstance(node, ast.alias):
        return f"<Alias: {node.name}, {node.asname}>"


    if type(node) in (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Module, ast.FunctionDef, ast.arguments,
                      ast.Store, ast.Load, ast.Pass, ast.Eq, ast.NotEq):
        #These either have no members, or no members we are currently interested in to print
        return f"<{str(type(node).__name__)}>"

    return str(node)


def _list_to_string(node_list):
    return str([node_to_string(item) for item in node_list])

