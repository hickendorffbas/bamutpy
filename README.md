

# Bamutpy: An in-memory mutation tester


This is a mutation tester for python that does do so completely in memory (no files are written). See https://en.wikipedia.org/wiki/Mutation_testing for an overview of what mutation testing is.

**WARNING:** Bamutpy (like other mutation testers) will randomly modify code and execute it, all risks of doing so are for the user!

**WARNING:** This is a tool I find useful for my own projects. It probably contains bugs. Running it is completely at your own risk. I don't promise it won't completely destroy your system by randomly running a mutated piece of code.





## Usage

First of all, I made this to do mutation testing on my own projects, so supporting those is my main goal. It might not work for your project setup. However, I'm happy to hear if it does not work for you, and look into a fix.

Currently there is no installable package, just make sure both bamutpy and the module your are testing are on your pythonpath.


### Is your project suitable?

Bamutpy is running all iterations in the same testsession (we import all modules and cache their originals and put them back after each test), so the tests must be repeatable in the same python session.

Tests are discovered in the standard python way, which makes it compatible with most ways of testing, but only in the most basic sense. For example, any pytest specific decorators are not supported.



## Configuration


Important properties to configure are "main_project_folder" and "test_module_folder". The first is the location of the code that will be mutated, the second is the tests that should be run against the mutations. Those paths can be the same (Bamutpy will not mutate testcode, so the test_module_folder can be inside the main_project_folder.


