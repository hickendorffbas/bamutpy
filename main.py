import ast
import copy
import glob
import os
import types

from bamutpy import config, mutator, scanner as scanner_module, test_runner
from bamutpy.config import get_config
from bamutpy.logger import log


#TODO: support 2 ways of usage: what mutations where not killed by any test, and what test was never unique in killing a mutant (i.e. detect redundant tests)


def file_path_to_import_path(project_root_path, file_path):
    if file_path[:len(project_root_path)] != project_root_path:
        raise Exception(f"filepath does not start with project_root_path (either of them is not absolute, or misconfigured). file_path: {file_path}, project_root_path: {project_root_path}")
    relative_file_path = file_path[len(project_root_path):]
    return relative_file_path.replace(".py", "").replace("/", ".")


def split_off_module_part_of_python_path(python_path):
    #TODO: Note that this currently needs to be in the main file for the scoping to work. 
    #      We can probably be smarter about where stuff that we eval / exec lives, scope wise (can I just pass the global scope?)
    potential_module_path = python_path
    while True:
        if isinstance(eval(potential_module_path), types.ModuleType):
            path_in_module = python_path.replace(potential_module_path, "").strip(".")
            return potential_module_path, path_in_module

        if "." not in potential_module_path:
            break
        potential_module_path = potential_module_path.rpartition('.')[0]

    raise Exception(f"No module found in path: {python_path}")


def find_all_test_files(test_module_folder):
    all_test_files = set()
    for filename in glob.iglob(test_module_folder + '/**/*_test.py', recursive=True):
        all_test_files.add(os.path.abspath(filename))
    for filename in glob.iglob(test_module_folder + '/**/test_*.py', recursive=True):
        all_test_files.add(os.path.abspath(filename))
    return all_test_files


def replace_member_in_module(python_path, mutated_module):
    module_part_of_python_path, path_in_module = split_off_module_part_of_python_path(python_path)

    if path_in_module:
        path_in_module = "." + path_in_module 

    global module_to_assign
    module_to_assign = mutated_module
    cmd = python_path + " = module_to_assign" + path_in_module
    exec(cmd)


config.Config.load()


scanner = scanner_module.SourceCodeScanner(get_config().main_project_folder, 
                                           get_config().test_module_folder)


all_test_modules = set()
test_module_idx = 1
for test_file in find_all_test_files(get_config().test_module_folder):

    module_name = f"test_module_{test_module_idx}"
    test_module = scanner_module.load_module(module_name, test_file)
    all_test_modules.add(test_module)

    # Make the testmodule available under its name with index
    global test_module_glob
    test_module_glob = test_module
    exec(module_name + " = test_module_glob")

    scanner.scan(test_module, module_name, test_file)

    test_module_idx += 1



for main_module_file_path in glob.iglob(get_config().main_project_folder + '*.py', recursive=False):

    module_name = main_module_file_path.partition(".")[0].split("/")[-1]
    our_module_alias = scanner_module.MAIN_MODULE_PREFIX + module_name
    main_module = scanner_module.load_module(our_module_alias, main_module_file_path)

    # Make the main module available under our alias
    global main_module_glob
    main_module_glob = main_module
    exec(our_module_alias + " = main_module_glob")



mutants_to_apply = mutator.generate_mutations(scanner, get_config().amount_of_mutations)

surviving_mutants = []
for mutant_to_apply in mutants_to_apply:

    log(f"applying {mutant_to_apply}")
    new_tree = copy.deepcopy(scanner.ast_tree_by_file[mutant_to_apply.file_path])
    mutator.CodeTransformer(mutant_to_apply).visit(new_tree)
    ast.fix_missing_locations(new_tree)
    mutated_module_code = compile(new_tree, filename="", mode="exec")

    mutated_module = types.ModuleType("mutated_module")
    exec(mutated_module_code, mutated_module.__dict__)

    python_path_of_mutated_module = file_path_to_import_path(get_config().main_project_folder, mutant_to_apply.file_path)

    for python_path, file_path in scanner.member_file_mapping.items():
        if file_path == mutant_to_apply.file_path:
            replace_member_in_module(python_path, mutated_module)

    mutant_alive = True
    for test_module in all_test_modules:
        if test_runner.has_failing_tests(test_module):
            mutant_alive = False

    if mutant_alive:
        log(f"Mutant ({mutant_to_apply}) is still alive after the tests!")
        surviving_mutants.append(mutant_to_apply)
    else:
        log(f"Mutant ({mutant_to_apply}) successfully killed")

    for python_path, file_path in scanner.member_file_mapping.items():
        if file_path == mutant_to_apply.file_path:
            replace_member_in_module(python_path, scanner.original_modules[mutant_to_apply.file_path])


print(f"{len(surviving_mutants)} out of {len(mutants_to_apply)} survived:")
for surviving_mutant in surviving_mutants:
    print(surviving_mutant)

