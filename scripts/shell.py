import sys
import os

# Add root directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flux.lexer import Lexer
from flux.parser import Parser
from flux.interpreter import Interpreter

def run(text, interp):
    tokens = Lexer(text).tokenize()
    ast = Parser(tokens).parse()
    return interp.visit(ast)

if __name__ == "__main__":
    interp = Interpreter()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            run(f.read(), interp)
    else:
        print("Flux 0.3 REPL")
        while True:
            text = input("Flux > ")
            if text == "exit": break
            print(run(text, interp))