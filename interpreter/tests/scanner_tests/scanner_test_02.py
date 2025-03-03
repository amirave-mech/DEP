import os

from interpreter.src.Scanner import Scanner

def test_scanner():
    source_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_file_03.txt"))
    
    with open(source_file, "r") as f:
        source_code = f.read()
    
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    
    for token in tokens:
        print(token)

if __name__ == "__main__":
    test_scanner()
