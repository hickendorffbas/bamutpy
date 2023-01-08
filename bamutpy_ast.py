import ast


def build_ast_from_file(file_path):
    with open(file_path, "r") as f:
        file_code = f.read()
    return parse_to_tree(file_code)


def parse_to_tree(code):
    tree = ast.parse(code)
    _set_parents(tree)
    return tree


def node_id(node):
    full_id = _single_node_to_partial_id(node)
    node_for_parent_check = node
    while node_for_parent_check.parent:
        full_id = _single_node_to_partial_id(node_for_parent_check.parent) + "." + full_id
        node_for_parent_check = node_for_parent_check.parent

    return full_id


def find_line_number(node):
    node_to_check = node
    while not hasattr(node_to_check, "lineno"):
        node_to_check = node_to_check.parent
        if node_to_check is None:
            return 0
    return node_to_check.lineno


def _set_parents(tree):
    for node in ast.walk(tree):
        if not hasattr(node, "parent"):
            node.parent = None
        for child in ast.iter_child_nodes(node):
            child.parent = node


def _single_node_to_partial_id(node):
    node_name = type(node).__name__

    if node.parent:
        all_childs_of_parent = []
        for field_name in node.parent._fields:
            field = eval("node.parent." + field_name)

            if isinstance(field, list):
                all_childs_of_parent.extend(field)
            else:
                all_childs_of_parent.append(field)

        node_idx = all_childs_of_parent.index(node)
        node_name = f"{node_name}({node_idx})"

    return node_name

