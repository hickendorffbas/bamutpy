import ast
import importlib.machinery
import inspect
import types

from bamutpy import bamutpy_ast
from bamutpy.logger import log


MAIN_MODULE_PREFIX = "bamutpy_main_module_"


def load_module(module_name, module_file):
    loader = importlib.machinery.SourceFileLoader(module_name, module_file)
    loaded_module = types.ModuleType(loader.name)
    loader.exec_module(loaded_module)
    return loaded_module


class ImportCollector(ast.NodeVisitor):

    def __init__(self):
        self.all_import_nodes_by_name = {}

    def visit_Import(self, node):
        for alias in node.names:
            self.all_import_nodes_by_name[self._get_alias_asname(alias)] = alias.name
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.all_import_nodes_by_name[self._get_alias_asname(alias)] = node.module + "." + alias.name
        self.generic_visit(node)

    def _get_alias_asname(self, alias):
        if alias.asname:
            return alias.asname
        return alias.name


class SourceCodeScanner():

    def __init__(self, main_project_folder, test_folder_path):
        self._main_project_folder = main_project_folder
        self._test_folder_path = test_folder_path
        self._files_scanned = set()

        self.ast_tree_by_file = {}
        self.member_file_mapping = {}
        self.original_modules = {}
        self.import_mappings = {}


    def scan(self, module, path_from_main_test_module, file_location_for_module):
        self._files_scanned.add(file_location_for_module)
        self._analyse_file(file_location_for_module)

        log(f"scanning {file_location_for_module}")

        if not file_location_for_module.startswith(self._test_folder_path):
            self.member_file_mapping[path_from_main_test_module] = file_location_for_module

        for member in inspect.getmembers(module):
            try:
                file_location_for_member = inspect.getfile(member[1])
            except TypeError:
                continue  #This happens for builtin types

            python_path_to_member = path_from_main_test_module + "." + member[0]

            if not file_location_for_member.startswith(self._test_folder_path):
                self.member_file_mapping[python_path_to_member] = file_location_for_member

            if isinstance(member[1], types.ModuleType):
                python_path_to_module = python_path_to_member
            else:
                potential_import_mapping = self.import_mappings[file_location_for_module].get(member[0])
                if potential_import_mapping:
                    python_path_to_module = MAIN_MODULE_PREFIX + self._file_path_to_import_path(file_location_for_member)
                else:
                    python_path_to_module = python_path_to_member[:-len(member[0])-1]

            if file_location_for_module != file_location_for_member:
                if file_location_for_member not in self._files_scanned:

                    member_module = load_module("member_module", file_location_for_member)
                    if not file_location_for_member.startswith(self._test_folder_path):
                        self.original_modules[file_location_for_member] = member_module

                    self.scan(member_module, python_path_to_module, file_location_for_member)


    def all_files(self):
        return set(self.member_file_mapping.values())

    def _file_path_to_import_path(self, file_path):
        path_in_project = file_path[len(self._main_project_folder):]
        return path_in_project.replace(".py", "").replace("/", ".")

    def _analyse_file(self, file_path):
        tree = bamutpy_ast.build_ast_from_file(file_path)
        self.ast_tree_by_file[file_path] = tree

        import_collector = ImportCollector()
        import_collector.visit(tree)

        self.import_mappings[file_path] = import_collector.all_import_nodes_by_name

