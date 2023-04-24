import re
import sys

from lexer import Lexer
from parser import Parser
from codegen import CodeGen
from compiler import Compiler

class CLI:

    def __init__(self):
        self.args = sys.argv
        self.props = {"keep": False}

    def main(self):
        if "-k" in self.args or "--keep" in self.args:
            self.props["keep"] = True
            
        for arg in self.args:
            if re.match("([A-z]*[0-9]*)*.na", arg):
                return self.run(arg)

        if "-h" in self.args or "--help" in self.args:
            print("""
usage: python3 natrium.py [src] [-h help] [-v version] [-k keep]

-v --version       Show version
-k --keep          Keep assembly files
-h --help          Print this help screen
            """)

        elif "-v" in self.args or "--version" in self.args:
            print("Natrium v0.0.1 Indev")



    def run(self, file_name):
        with open(file_name, "r") as f:
            src = "\n".join(map(str, f.readlines()))

            lexer = Lexer(src)
            toks, err = lexer.tokenize()
            if err: return print(err.fmt(src, file_name))

            parser = Parser(toks)
            parser_res = parser.parse()
            if parser_res.error: return print(parser_res.error.fmt(src, file_name))

            code_gen = CodeGen()
            code_gen_res = code_gen.visit(parser_res.node)
            code_gen_res.generate()

            compiler = Compiler(code_gen_res.code, file_name.split(".")[0], self.props)
            compiler.compile()