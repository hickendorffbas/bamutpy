import inspect
import os
import sys


def has_failing_tests(test_module):

    all_class_members = inspect.getmembers(test_module, inspect.isclass)
    for class_name, class_member in all_class_members:
        if class_name.startswith("Test"):

            function_members_on_class = inspect.getmembers(class_member, inspect.isfunction)
            for name, member in function_members_on_class:
                if name.startswith("test_"):
                    _block_output()
                    try:
                        member(class_member())
                    except:
                        # we are catching all exceptions here on purpose, if the test failed in any way (including assertions), we killed the mutant
                        return True
                    finally:
                        _unblock_output()

    all_function_members = inspect.getmembers(test_module, inspect.isfunction)
    for name, member in all_function_members:
        if name.startswith("test_"):
            _block_output()
            try:
                member()
            except:
                # we are catching all exceptions here on purpose, if the test failed in any way (including assertions), we killed the mutant
                return True
            finally:
                _unblock_output()

    return False


def _block_output():
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')


def _unblock_output():
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
