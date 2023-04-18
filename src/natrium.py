"""
================
  LICENSE: MIT
================

Copyright 2023 Azrac Studios

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the “Software”), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
DEALINGS IN THE SOFTWARE.
"""

###############
### IMPORTS ###
###############
import re
import sys
import os

#############
### UTILS ###
#############


def check_type(object, _type):
    return type(object).__name__ == _type.__name__


## COLORS
# REF: https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html


# Generates python code for standard ANSI color codes along with a basic test
# PS: I am too lazy to write the functions out myself :)
def color_generator():
    colors = [
        "black",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
        "white",
    ]

    code = ""
    for i, color in enumerate(colors):
        code += f"""
def {color}(string: str):
    return f"\\u001b[{30 + i}m{"{string}"}\\u001b[0m"

def bright_{color}(string: str):
    return f"\\u001b[{30 + i};1m{"{string}"}\\u001b[0m"
        """

    code += "\ndef test_colors(string: str):\n"
    for color in colors:
        code += f"""
    print({color}(string))
    print(bright_{color}(string))
        """

    return code


def black(string: str):
    return f"\u001b[30m{string}\u001b[0m"


def bright_black(string: str):
    return f"\u001b[30;1m{string}\u001b[0m"


def red(string: str):
    return f"\u001b[31m{string}\u001b[0m"


def bright_red(string: str):
    return f"\u001b[31;1m{string}\u001b[0m"


def green(string: str):
    return f"\u001b[32m{string}\u001b[0m"


def bright_green(string: str):
    return f"\u001b[32;1m{string}\u001b[0m"


def yellow(string: str):
    return f"\u001b[33m{string}\u001b[0m"


def bright_yellow(string: str):
    return f"\u001b[33;1m{string}\u001b[0m"


def blue(string: str):
    return f"\u001b[34m{string}\u001b[0m"


def bright_blue(string: str):
    return f"\u001b[34;1m{string}\u001b[0m"


def magenta(string: str):
    return f"\u001b[35m{string}\u001b[0m"


def bright_magenta(string: str):
    return f"\u001b[35;1m{string}\u001b[0m"


def cyan(string: str):
    return f"\u001b[36m{string}\u001b[0m"


def bright_cyan(string: str):
    return f"\u001b[36;1m{string}\u001b[0m"


def white(string: str):
    return f"\u001b[37m{string}\u001b[0m"


def bright_white(string: str):
    return f"\u001b[37;1m{string}\u001b[0m"


def test_colors(string: str):

    print(black(string))
    print(bright_black(string))

    print(red(string))
    print(bright_red(string))

    print(green(string))
    print(bright_green(string))

    print(yellow(string))
    print(bright_yellow(string))

    print(blue(string))
    print(bright_blue(string))


################
### ASSEMBLY ###
################
ASM_BASE = """
section .bss
digitSpace resb 100
digitSpacePos resb 8
section .text
global _start
_printNum:
mov rcx, digitSpace
mov rbx, 10
mov [rcx], rbx
inc rcx
mov [digitSpacePos], rcx
_printNumLoop:
mov rdx, 0
mov rbx, 10
div rbx
push rax
add rdx, 48
mov rcx, [digitSpacePos]
mov [rcx], dl
inc rcx
mov [digitSpacePos], rcx
pop rax
cmp rax, 0
jne _printNumLoop
_printNumLoop2:
mov rcx, [digitSpacePos]
mov rax, 1
mov rdi, 1
mov rsi, rcx
mov rdx, 1
syscall
mov rcx, [digitSpacePos]
dec rcx
mov [digitSpacePos], rcx
cmp rcx, digitSpace
jge _printNumLoop2
ret
_start:
"""

ASM_EXIT = """
call _printNum
mov rax, 60
mov rdi, 0
syscall
"""

#############
### ERROR ###
#############
ERR_LEX = "Illegal Character"
ERR_PAR = "Parser Error"


class Error:

    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def fmt(self, src, file_name):
        result = bright_red(
            f'{self.error_name} @ Ln {self.pos_start.ln + 1}, Col {self.pos_start.col}\n'
        )
        result += f"{bright_white(file_name)}: {self.details}\n\n"

        idx_start = max(src.rfind('\n', 0, self.pos_start.idx), 0)
        idx_end = src.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(src)

        line_count = self.pos_end.ln - self.pos_start.ln + 1
        max_ln_num_len = len(str(line_count))

        for i in range(line_count):
            line = src[idx_start:idx_end]
            col_start = self.pos_start.col if i == 0 else 0
            col_end = self.pos_end.col if i == line_count - 1 else len(
                line) - 1

            space_width = max_ln_num_len - len(str(i)) + 1
            result += bright_black(f"{i + 1}{' ' * space_width}| ")
            result += white(line + '\n')
            result += bright_red(' ' * (col_start + max_ln_num_len + 3) + '^' *
                                 (col_end - col_start))

            idx_start = idx_end
            idx_end = src.find('\n', idx_start + 1)
            if idx_end < 0: idx_end = len(src)

        return result.replace('\t', '')


class IllegalCharError(Error):

    def __init__(self, pos_start, pos_end, char):
        super().__init__(pos_start, pos_end, ERR_LEX, char)


class InvalidSyntaxError(Error):

    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, ERR_PAR, details)


################
### POSITION ###
################
class Position:

    def __init__(self, idx, col, ln):
        self.idx = idx
        self.col = col
        self.ln = ln

    def advance(self, char=None):
        self.idx += 1
        self.col += 1

        if char == "\n":
            self.col = 0
            self.ln += 1

        return self

    def copy(self):
        return Position(self.idx, self.col, self.ln)

    def line_begin(self):
        return Position(0, 0, self.ln)

    def __repr__(self):
        return f"Ln {self.ln}, Col {self.col}"


#############
### TOKEN ###
#############
TT_INT = "INT"
TT_FLOAT = "FLOAT"

TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_POW = "POW"

TT_NEWLINE = "NEWLINE"


class Token:

    def __init__(self, type, start_position, value=None, end_position=None):
        self.type = type
        self.value = value
        self.start_position = start_position.copy()
        self.end_position = (end_position or start_position).copy()

    def matches(self, type, value=None):
        return self.type == type or (self.type == type and self.value == value)

    def __repr__(self):
        return f"{self.type}{f': {self.value}' if self.value else '' }"


########################
### LEXICAL ANALYSIS ###
########################


class Lexer:

    def __init__(self, src):
        self.src: str = src
        self.char: str = None
        self.position: Position = Position(-1, -1, 0)
        self.tokens: List[Token] = []
        self.should_advance_next_ittr: bool = True
        self.advance()

    def advance(self):
        self.position.advance(self.char)

        if self.position.idx < len(self.src):
            self.char = self.src[self.position.idx]
        else:
            self.char = None

    def next(self) -> Token:
        # NEWLINE
        if self.char == "\n":
            return Token(TT_NEWLINE, self.position)

        # SPACE
        if self.char == " ":
            return None

        ## LPAREN
        if self.char == "(":
            return Token(TT_LPAREN, self.position)

        ## RPAREN
        if self.char == ")":
            return Token(TT_RPAREN, self.position)

        ## PLUS
        if self.char == "+":
            return Token(TT_PLUS, self.position)

        ## MINUS
        if self.char == "-":
            return Token(TT_MINUS, self.position)

        ## MUL
        if self.char == "*":
            return Token(TT_MUL, self.position)

        ## DIV
        if self.char == "/":
            return Token(TT_DIV, self.position)

        ## POW
        if self.char == "^":
            return Token(TT_POW, self.position)

        ## INT | FLOAT
        if re.match("[0-9]", self.char):
            num_str = ""
            start_position = self.position.copy()
            is_float = False

            while re.match("[0-9]|\.", self.char or "EOF"):
                if self.char == ".":
                    if is_float:
                        print("ERR OCCOURED")
                        return

                    is_float = True

                num_str += self.char
                self.advance()

            tok_type = TT_FLOAT if is_float else TT_INT
            self.should_advance_next_ittr = False
            return Token(
                tok_type,
                start_position,
                end_position=self.position.copy(),
                value=float(num_str) if is_float else int(num_str),
            )

    def tokenize(self):
        while self.char != None:
            next = self.next()

            if next != None:
                self.tokens.append(next)
            elif self.char != " ":
                return IllegalCharError(self.position.copy(),
                                        self.position.copy().advance(),
                                        self.char)

            if self.should_advance_next_ittr:
                self.advance()
            else:
                self.should_advance_next_ittr = True

        return self.tokens


##########################
### SYNTACTIC ANALYSIS ###
##########################


class NumberNode:

    def __init__(self, token: Token):
        self.token: Token = token
        self.start_position: Position = self.token.start_position
        self.end_position: Position = self.token.end_position

    def __repr__(self) -> str:
        return f"{self.token.value}"


class UnaryOperatorNode:

    def __init__(self, left, value):
        self.left = left
        self.value = value
        self.start_position: Position = self.left.start_position
        self.end_position: Position = self.value.end_position

    def __repr__(self):
        return f"({self.left} {self.value})"


class BinaryOperatorNode:

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        self.start_position: Position = self.left.start_position
        self.end_position: Position = self.right.end_position

    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"


class ParseRegister:

    def __init__(self, advance):
        self.error, self.node, self.expected_end = None, None, None
        self.advance = advance
        self.advance_count = 0

    def register(self, res):
        if res.error: self.error = res.error
        return res.node

    def register_advance(self):
        self.advance_count += 1
        self.advance()

    def register_expected_end(self, end):
        self.expected_end = end

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self


class Parser:

    def __init__(self, tokens):
        self.tokens: List[Token] = tokens
        self.cur_tok: Token | None = None
        self.idx = -1
        self.advance()

    def advance(self):
        self.idx += 1

        if self.idx < len(self.tokens):
            self.cur_tok = self.tokens[self.idx]

    def parse(self):
        return self.expr()

    # NUMBER
    def factor(self):
        res = ParseRegister(self.advance)
        tok = self.cur_tok
        res.register_expected_end(tok)

        if tok.type == TT_INT or tok.type == TT_FLOAT:
            res.register_advance()
            return res.success(NumberNode(tok))

        if tok.type == TT_LPAREN:
            res.register_expected_end(self.cur_tok)
            res.register_advance()

            expr = res.register(self.expr())
            if res.error: return res
            res.register_expected_end(self.cur_tok)

            if not self.cur_tok.matches(TT_RPAREN):
                return res.failure(
                    InvalidSyntaxError(self.cur_tok.start_position,
                                       self.cur_tok.start_position,
                                       "Expected ')'"))
            res.register_advance()

            return res.success(expr)

        return res.failure(
            InvalidSyntaxError(tok.start_position.copy().line_begin(),
                               tok.start_position.copy().advance().advance(),
                               "Incomplete Expression"))

    # FACTOR ((MUL | DIV) FACTOR)*
    def term(self):
        return self.binop(self.factor, (TT_MUL, TT_DIV))

    # TERM ((PLUS | MINUS) TERM)*
    def expr(self):
        return self.binop(self.term, (TT_PLUS, TT_MINUS))

    # LFT_FUNC ((...OPS) RT_FUNC)*
    def binop(self, func, ops):
        res = ParseRegister(self.advance)

        lft = res.register(func())
        if res.error: return res

        while self.cur_tok.type in ops:
            op = self.cur_tok
            res.register_advance()

            rt = res.register(func())
            if res.error: return res

            lft = BinaryOperatorNode(lft, op, rt)

        return res.success(lft)


###################################
### INTERMEDIATE REPRESENTATION ###
###################################


class NumberIR:

    def __init__(self, node):
        self.node = node
        self.code = ""

    def generate(self):
        self.code = f"{self.node.token.value}"
        return self


class BinaryOperatorIR:

    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        self.code = ""

    def generate(self):
        left = self.left.generate()
        op = self.operator.type
        right = self.right.generate()

        if check_type(left, BinaryOperatorIR):
            self.code += left.code

            ## a:BINOP_IR op b:BINOP_IR
            ## compute a
            ## result of a -> rcx
            ## compute b
            ## result of b -> rbx
            ## result of a in rcx -> rax
            ## compute (a op b)
            ## result (a op b) -> rax
            if check_type(right, BinaryOperatorIR):
                self.code += f"mov rcx, rax\n"
                self.code += right.code
                self.code += "mov rbx, rax\n"
                self.code += "mov rax, rcx\n"
                if op == TT_PLUS:
                    self.code += f"add rax, rbx\n"
                if op == TT_MINUS:
                    self.code += f"sub rax, rbx\n"
                if op == TT_MUL:
                    self.code += f"mul rbx\n"
                if op == TT_DIV:
                    self.code += f"div rbx\n"

        
        if check_type(left, NumberIR):
            ## a:NUMBER_IR op b:BINOP_IR
            ## compute b
            ## result of b in rax -> rcx
            ## number a -> rax
            ## compute (a op b)
            ## result (a op b) -> rax
            if check_type(right, BinaryOperatorIR):
                self.code += right.code
                self.code += f"mov rcx, rax\n"
                self.code += f"mov rax, {left.code}\n"
                if op == TT_PLUS:
                    self.code += f"add rax, rcx\n"
                if op == TT_MINUS:
                    self.code += f"sub rax, rcx\n"
                if op == TT_MUL:
                    self.code += f"mul rcx\n"
                if op == TT_DIV:
                    self.code += f"div rcx\n"

            ## number a -> rax
            else:
                self.code += f"mov rax, {left.code}\n"

        
        ## a:NUMBER_IR op b:NUMBER_IR
        ## number a -> rax
        ## number b -> rbx ?
        ## compute (a op b)
        ## result (a op b) -> rax
        if check_type(right, NumberIR):
            if op == TT_PLUS:
                self.code += f"add rax, {right.code}\n"
            if op == TT_MINUS:
                self.code += f"sub rax, {right.code}\n"
            if op == TT_MUL:
                self.code += f"mov rbx, {right.code}\n"
                self.code += f"mul rbx\n"
            if op == TT_DIV:
                self.code += f"mov rbx, {right.code}\n"
                self.code += f"div rbx\n"

        return self


#######################
### CODE GENERATION ###
#######################


class CodeGen:

    def visit(self, ast):
        return self.__getattribute__(f"visit_{type(ast).__name__}")(ast)

    def visit_NumberNode(self, node):
        return NumberIR(node)

    def visit_BinaryOperatorNode(self, node):
        left = self.visit(node.left)
        operator = node.operator
        right = self.visit(node.right)

        return BinaryOperatorIR(left, operator, right)


################
### COMPILER ###
################


class Compiler:

    def __init__(self, code, file_name):
        self.code = code
        self.file_name = file_name

    def generate_final(self):
        return ASM_BASE + self.code + ASM_EXIT

    def write_out(self):
        file_name = f"{self.file_name}.asm"
        os.system(f"touch {file_name}")

        with open(file_name, "w") as f:
            f.write(self.code)

    def compile(self):
        self.code = self.generate_final()
        self.write_out()

        os.system(f"nasm -f elf64 -o {self.file_name}.o {self.file_name}.asm")
        os.system(f"ld -o {self.file_name} {self.file_name}.o")
        os.system(f"rm {self.file_name}.o {self.file_name}.asm")


###########
### CLI ###
###########


class CLI:

    def __init__(self):
        self.args = sys.argv

    def main(self):
        for arg in self.args:
            if re.match("([A-z]*[0-9]*)*.na", arg):
                return self.run(arg)

        if "-h" in self.args or "--help" in self.args:
            print("usage: python3 natrium.py [src] [-h help]")

        elif "-v" in self.args or "--version" in self.args:
            print("Natrium v0.0.1 Indev")

    def run(self, file_name):
        with open(file_name, "r") as f:
            src = "\n".join(map(str, f.readlines()))

            lexer = Lexer(src)
            toks = lexer.tokenize()

            if type(toks).__name__ == "IllegalCharError":
                return print(toks.fmt(src, file_name))

            parser = Parser(toks)
            parser_res = parser.parse()
            if parser_res.error:
                return print(parser_res.error.fmt(src, file_name))

            code_gen = CodeGen()
            code_gen_res = code_gen.visit(parser_res.node)
            code_gen_res.generate()

            compiler = Compiler(code_gen_res.code, file_name.split(".")[0])
            compiler.compile()

cli = CLI()
cli.main()