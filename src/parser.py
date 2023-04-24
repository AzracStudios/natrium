from parsernodes import *
from token import *
from error import InvalidSyntaxError

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