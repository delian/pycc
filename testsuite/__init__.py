import os
from cc import Compiler


def run_tests():
    test_files = [f for f in os.listdir("data") if f.endswith(".pcc")]
    for test_file in test_files:
        with open(f"data/{test_file}") as f:
            test = f.read()
            print("-----------------------------------------------")
            c = Compiler(test)
            c.compile_module(test)
    print("All tests passed!")
