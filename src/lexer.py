import re
from token import *
from error import IllegalCharError

class Lexer:

    def __init__(self, src):
        self.src = src
        self.char = None
        self.position = Position(-1, -1, 0)
        self.tokens = []
        self.should_advance_next_ittr = True
        self.advance()

    def advance(self):
        self.position.advance(self.char)

        if self.position.idx < len(self.src):
            self.char = self.src[self.position.idx]
        else:
            self.char = None

    def next(self):
        # NEWLINE
        if self.char == "\n":
            return Token(TT_NEWLINE, self.position), None

        # SPACE
        if self.char == " ":
            return Token(TT_SPACE, self.position), None

        ## LPAREN
        if self.char == "(":
            return Token(TT_LPAREN, self.position), None

        ## RPAREN
        if self.char == ")":
            return Token(TT_RPAREN, self.position), None

        ## PLUS
        if self.char == "+":
            return Token(TT_PLUS, self.position), None

        ## MINUS
        if self.char == "-":
            return Token(TT_MINUS, self.position), None

        ## MUL
        if self.char == "*":
            return Token(TT_MUL, self.position), None

        ## DIV
        if self.char == "/":
            return Token(TT_DIV, self.position), None

        ## POW
        if self.char == "^":
            return Token(TT_POW, self.position), None

        ## INT | FLOAT
        if re.match("[0-9]", self.char):
            num_str = ""
            start_position = self.position.copy()
            is_float = False

            # nums 0 through 9 or a decimal point
            while re.match("[0-9]|\.", self.char or "EOF"):
                if self.char == ".":
                    if is_float:
                        return None, IllegalCharError(self.position.copy(), self.position.copy.advance(), ".")

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
            ), None

    def tokenize(self):
        while self.char != None:
            next, err = self.next()
            if err: return None, err

            if next.type != TT_SPACE:
                self.tokens.append(next)
            
            if self.should_advance_next_ittr:
                self.advance()
            else:
                self.should_advance_next_ittr = True

        return self.tokens, None