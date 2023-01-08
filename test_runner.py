import inspect


def has_failing_tests(test_module):

    all_class_members = inspect.getmembers(test_module, inspect.isclass)
    for class_name, class_member in all_class_members:
        if class_name.startswith("Test"):

            function_members_on_class = inspect.getmembers(class_member, inspect.isfunction)
            for name, member in function_members_on_class:
                if name.startswith("test_"):
                    try:
                        member(class_member())
                    except:
                        # we are catching all exceptions here on purpose, if the test failed in any way (including assertions), we killed the mutant
                        return True

    all_function_members = inspect.getmembers(test_module, inspect.isfunction)
    for name, member in all_function_members:
        if name.startswith("test_"):
            try:
                member()
            except:
                # we are catching all exceptions here on purpose, if the test failed in any way (including assertions), we killed the mutant
                return True

    return False

