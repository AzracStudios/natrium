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
TT_SPACE = "SPACE"


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
