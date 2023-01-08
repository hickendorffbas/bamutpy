from bamutpy import bamutpy_ast, scanner



def test_import_collector():

    tree = bamutpy_ast.build_ast_from_file("tests/testproject/tests/test_bank.py")

    import_collector = scanner.ImportCollector()
    import_collector.visit(tree)

    assert import_collector.all_import_nodes_by_name == {"bank": "testproject.bank.bank", "main": "testproject.main", "open_account": "testproject.main.open_account"}




def test_import_collector_with_as_import():

    tree = bamutpy_ast.build_ast_from_file("tests/testproject/bank/account.py")

    import_collector = scanner.ImportCollector()
    import_collector.visit(tree)

    assert import_collector.all_import_nodes_by_name == {"loan_module": "testproject.bank.loan"}

